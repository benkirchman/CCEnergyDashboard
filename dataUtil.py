import pyodbc
import datetime
import pandas as pd
import h5py
import dbInfo

startDate = datetime.datetime(2018,1,1) # Date from which we assume good data
# TODO: Change this value to the first day with continuously good data since.
heatFactor = 1.67
elecFactor = .25
heatToCarbonFactor = .000053163
elecToCarbonFactor = .000914
heatToElecFactor = .2930832
boilerEfficiency = 1.67
solarCreditFactor = .000830
solarTables = ['CCWS_TuttLibrary_Wattnode__MDP__A_Consumption__DL']

def getCursor():
    server = dbInfo.server
    database = dbInfo.database
    username = dbInfo.username
    password = dbInfo.password
    cnxn = pyodbc.connect('DRIVER=FreeTDS;SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return cnxn.cursor()

def executeCursor(table, minDate):
        cursor = getCursor()
        queryStr = """SELECT * FROM hvaclogging.dbo.%s
                    WHERE tstamp > ? """ % (table)
        cursor.execute(queryStr, minDate)
        return cursor.fetchall()




def sumDataFramesByTimeStamp(df1, df2):
    df3 = pd.merge(df1, df2, on=['timeStamp'])
    df3['value'] = df3['value_x'] + df3['value_y']
    df4 = df3.loc[:,['timeStamp', 'value']]
    return df4

def getDFSum(df, intervalValue):
    if intervalValue == 'CUM' or intervalValue == 'MIN':
        return df
    elif intervalValue == 'HOU':
        val = df.groupby(df['timeStamp'].dt.hour).sum().reset_index()
        return val
    elif intervalValue == 'WEE':
        return df.groupby(df['timeStamp'].dt.week).sum().reset_index()
    elif intervalValue == 'DOW':
        return df.groupby(df['timeStamp'].dt.dayofweek).sum().reset_index()
    elif intervalValue == 'QUA':
        return df.groupby(df['timeStamp'].dt.quarter).sum().reset_index()
    elif intervalValue == 'MON':
        return df.groupby(df['timeStamp'].dt.month).sum().reset_index()
    elif intervalValue == 'ANN':
        return df.groupby(df['timeStamp'].dt.year).sum().reset_index()
    elif intervalValue == 'DAY':
        return df.groupby(df['timeStamp'].dt.date).sum().reset_index()

def getDataFrame(table, minDate = startDate, maxValue = 1000, factor = 1, negativeFactor = None):
    values = []
    timeStamps = []
    rows = executeCursor(table, minDate)
    for row in rows:
        if row.tstamp > minDate and abs(row.value) < maxValue:
            if negativeFactor and row.value < 0:
                values.append(row.value * negativeFactor)
            else:
                values.append(row.value * factor)
            truncated = row.tstamp.replace(second=0, microsecond=0)
            timeStamps.append(truncated)
    df = pd.DataFrame({'timeStamp': timeStamps, 'value': values})
    df = df.sort_values(by=['timeStamp'])
    return df

def getDFWithCache(table, dataType, type, minDate = startDate):
    with pd.HDFStore('store.h5') as store:
        try:
            vals = store[table+dataType]
            lastDate = vals['timeStamp'].iloc[-1]
            lastAcceptableValue = datetime.datetime.now() - datetime.timedelta(hours=5)
            print("found entry", lastDate)
            if lastDate < lastAcceptableValue:
                print("updating- retrieving data")
                newVals = getDF(table, dataType, type, lastDate)
                if newVals is not None and len(newVals) != 0:
                    print("updating- adding new data")
                    vals = vals.append(newVals)
                    maxDate = vals['timeStamp'].iloc[-1]
                    store[table+dataType] = vals
            if minDate != startDate:
                mask = (vals['timeStamp'] > minDate)
                return vals.loc[mask]
            return vals
        except KeyError:
            print("CACHE MISS")
            vals = getDF(table, dataType, type, startDate)
            store[table+dataType] = vals
            return vals

# returns the dataframe with the type provided
def getDF(table, dataType, type, minDate = startDate):
    factor = 1

    #modify factor based on output type
    if dataType == 'ENER':
        if type == 'HEAT':
            factor = heatToElecFactor
    elif dataType == 'CARB':
        if type == 'ELEC':
            factor = elecToCarbonFactor
        elif type == 'HEAT':
            factor = heatToCarbonFactor
        elif type == 'NGAS':
            factor = heatToCarbonFactor

    #modify factor based on dataType
    if type == 'ELEC':
        factor *= .25
    elif type == 'HEAT':
        factor *= boilerEfficiency

    #Modify negativeFactor for solar tables
    negativeFactor = factor
    if table in solarTables:
        negativeFactor = (.25 * .000830)

    return getDataFrame(table, factor = factor, negativeFactor = negativeFactor, minDate = minDate)

def sumDataframes(dfs):
    if len(dfs) == 0:
        return None
    counter = 0
    while counter < len(dfs) - 1:
        dfs[counter+1] = sumDataFramesByTimeStamp(dfs[counter], dfs[counter + 1])
        counter += 1

    return dfs[counter]
