import datetime
import pandas as pd

tablesDict = [{'value': 'ANT', 'name':'Blanca_lonTrunk_Wattnode__Antero_Consumption__DL', 'type': 'ELEC'},
              {'value': 'ARM', 'name':'Armstrong_lonTrunk_WattNode_Consumption__DL', 'type': 'ELEC'},
              {'value': 'ARM', 'name':'Armstrong_ModbusAsyncNetwork_ArmstrongBTUmeter_Temp_CHW__KBTU__DL__TTL', 'type': 'HEAT'},
              {'value': 'ARM', 'name':'Armstrong_ModbusAsyncNetwork_ArmstrongBTUmeter_Temp_HTHW__KBTU__DL', 'type': 'HEAT'},
              {'value': 'ART', 'name':'OlinHall_lonTrunk_Wattnode__Arthur_Consumption__DL', 'type': 'ELEC'},
              {'value': 'BEM', 'name':'CCHP_lonTrunk_WattNode__Bemis_Consumption__DL', 'type': 'ELEC'},
              {'value': 'BLA', 'name':'Blanca_lonTrunk_Wattnode__Blanca_Consumption__DL', 'type': 'ELEC'},
              {'value': 'BOE', 'name':'Boettcher__Health__Center_lonTrunk_Wattnode__Boettcher_Consumption__DL', 'type': 'ELEC'},
              {'value': 'FAC', 'name':'CCWS_FineArtsCenter_Wattnode__FAC_Consumption__DL', 'type': 'ELEC'},
              {'value': 'FAC', 'name':'CCWS_FineArtsCenter_Wattnode__BSA_Consumption__DL', 'type': 'ELEC'},
              {'value': 'CUT', 'name':'CCHP_lonTrunk_WattNodeCutler_Consumption__DL', 'type': 'ELEC'},
              {'value': 'EAS', 'name':'CCWS_EastCampusHousing_Wattnode__Bldg2_Consumption__DL', 'type': 'ELEC'},
              {'value': 'EAS', 'name':'CCWS_EastCampusHousing_Wattnode__Bldg3_Consumption__DL', 'type': 'ELEC'},
              {'value': 'EAS', 'name':'CCWS_EastCampusHousing_Wattnode__Bldg4_Consumption__DL', 'type': 'ELEC'},
              {'value': 'EAS', 'name':'CCWS_EastCampusHousing_Wattnode__Bldg5_Consumption__DL', 'type': 'ELEC'},
              {'value': 'GAY', 'name':'Boettcher__Health__Center_lonTrunk_WattNode__EdithGaylord_Consumption__DL', 'type': 'ELEC'},
              {'value': 'CNR', 'name':'CCWS_Cornerstone_Electric__Main_Consumption__DL', 'type': 'ELEC'},
              {'value': 'CNR', 'name':'CCWS_Cornerstone_PlantEnergyIn_CHW__KBTU__DL__TTL', 'type': 'HEAT'},
              {'value': 'CNR', 'name':'CCWS_Cornerstone_PlantEnergyIn_HTHW__KBTU__DL', 'type': 'HEAT'},
              {'value': 'ELD', 'name':'CCWS_ElDiente_Electric__Main_Consumption__DL', 'type': 'ELEC'},
              {'value': 'POM', 'name':'SwimmingPool_lonTrunk_WattNode__ElPomar_Consumption__DL', 'type': 'ELEC'},
              {'value': 'POM', 'name':'CCHP_ModbusAsyncNetwork_ModbusAsyncDevice_Temp_ElPomar__KBTU__DL', 'type': 'HEAT'},
              {'value': 'POM', 'name':'ChillerPlant_ModbusAsyncNetwork_ElPomarCHW__BTUmeter_Temp_CHW__KBTU__DL__TTL', 'type': 'HEAT'},
              {'value': 'HON', 'name':'ChillerPlant_lonTrunk_WattNote__Honnen_Consumption__DL', 'type': 'ELEC'},
              {'value': 'WOR', 'name':'WornerCenter_LonTrunk_WattNode__Main_Consumption__DL', 'type': 'ELEC'},
              {'value': 'WOR', 'name':'WornerCenter_ModbusAsyncNetwork_BTUmeter_Temp_CHW__KBTU__DL__TTL', 'type': 'HEAT'},
              {'value': 'WOR', 'name':'WornerCenter_ModbusAsyncNetwork_BTUmeter_Temp_HTHW__KBTU__DL', 'type': 'HEAT'},
              {'value': 'JLK', 'name':'Blanca_lonTrunk_Wattnode__JLK__Main_Consumption__DL', 'type': 'ELEC'},
              {'value': 'LOO', 'name':'Boettcher__Health__Center_lonTrunk_WattNode__Loomis_Consumption__DL2', 'type': 'ELEC'},
              {'value': 'LOO', 'name':'Boettcher__Health__Center_ModbusAsyncNetwork_LoomisBTUmeter_Temp_CHW__KBTU__DL', 'type': 'HEAT'},
              {'value': 'LOO', 'name':'Boettcher__Health__Center_ModbusAsyncNetwork_LoomisBTUmeter_Temp_HTHW__KBTU__DL', 'type': 'HEAT'},
              {'value': 'MAT', 'name':'OlinHall_lonTrunk_WattNode__MathiasMain_Consumption__DL', 'type': 'ELEC'},
              {'value': 'MAT', 'name':'CCWS_Mathias_PlantEnergyIn_HTHW__KBTU__DL', 'type': 'HEAT'},
              {'value': 'MAT', 'name':'CCWS_Mathias_PlantEnergyIn_CHW__KBTU__DL__TTL', 'type': 'HEAT'},
              {'value': 'MCG', 'name':'Blanca_lonTrunk_Wattnode__McGregor_Consumption__DL', 'type': 'ELEC'},
              {'value': 'MCG', 'name':'Blanca_ModbusAsyncNetwork_McGregorBTUmeter_Temp_McGregor__LTHW__KBTU__DL', 'type': 'HEAT'},
              {'value': 'MON', 'name':'CCHP_lonTrunk_WattNode__Montgomery_Consumption__DL', 'type': 'ELEC'},
              {'value': 'OLI', 'name':'OlinHall_lonTrunk_WattNode__Olin_Consumption__DL', 'type': 'ELEC'},
              {'value': 'OLI', 'name':'CCWS_OlinHall_PlantEnergyIn_CHW__KBTU__DL__TTL', 'type': 'HEAT'},
              {'value': 'OLI', 'name':'OlinHall_ModbusAsyncNetwork_OlinBTUmeter_Temp_Olin__HTHW__KBTU__DL', 'type': 'HEAT'},
              {'value': 'PAL', 'name':'CCWS_Palmer_Wattnode__Main_Consumption__DL', 'type': 'ELEC'},
              {'value': 'PAL', 'name':'CCWS_Palmer_PlantEnergyIn_CHW__KBTU__DL__TTL', 'type': 'HEAT'},
              {'value': 'PAL', 'name':'CCWS_Palmer_PlantEnergyIn_HTHW__KBTU__DL', 'type': 'HEAT'},
              {'value': 'TUT', 'name':'CCWS_TuttScienceCenter_Wattnode__Main_Consumption__DL', 'type': 'ELEC'},
              {'value': 'TUT', 'name':'CCWS_TuttScienceCenter_PlantEnergyIn_CHW__KBTU__DL__TTL', 'type': 'HEAT'},
              {'value': 'TUT', 'name':'CCWS_TuttScienceCenter_PlantEnergyIn_HTHW__KBTU__DL', 'type': 'HEAT'},
              {'value': 'TLB', 'name':'CCWS_TuttLibrary_Wattnode__MDP__A_Consumption__DL', 'type': 'ELEC'},
              {'value': 'TLB', 'name':'CCWS_TuttLibrary_Wattnode__MDP__B_Consumption__DL', 'type': 'ELEC'},
              {'value': 'TLB', 'name':'CCWS_TuttLibrary_NGas__and__Totals_Consumption__DL__NGas', 'type': 'NGAS'},
              {'value': 'TLB', 'name':'CCWS_TuttLibrary_PlantEnergyIn__Heat_HTHW__KBTU__DL__HTHW', 'type': 'HEAT'},
              {'value': 'SHC', 'name':'Shove_lonTrunk_WattNode__Shove_Consumption__DL', 'type': 'ELEC'},
              {'value': 'SOU', 'name':'Armstrong_lonTrunk_WattNode__Slocum_Consumption__DL', 'type': 'ELEC'},
              {'value': 'SOU', 'name':'Armstrong_ModbusAsyncNetwork_SlocumBTUmeter_Temp_CHW__KBTU__DL__TTL', 'type': 'HEAT'},
              {'value': 'SOU', 'name':'Armstrong_ModbusAsyncNetwork_SlocumBTUmeter_Temp_HTHW__KBTU__DL__15min', 'type': 'HEAT'},
              {'value': 'PAC', 'name':'CCWS_PackardHall_Wattnode__Main_Consumption__DL', 'type': 'ELEC'},
              {'value': 'PAC', 'name':'CCWS_PackardHall_PlantEnergyIn_CHW__KBTU__DL__TTL', 'type': 'HEAT'},
              {'value': 'PAC', 'name':'CCWS_PackardHall_PlantEnergyIn_HTHW__KBTU__DL', 'type': 'HEAT'},
              {'value': 'TIC', 'name':'CCHP_lonTrunk_WattNode__Ticknor_Consumption__DL', 'type': 'ELEC'},
              {'value': 'SPE', 'name':'CCWS_Spencer_Wattnode__Main_Consumption__DL', 'type': 'ELEC'},
              {'value': 'SPE', 'name':'CCWS_Spencer_PlantEnergyIn_HTHW__KBTU__DL', 'type': 'ELEC'},
              {'value': 'SPE', 'name':'CCWS_Spencer_PlantEnergyIn_CHW__KBTU__DL__TTL', 'type': 'ELEC'}]


# type is one of 'RES': residential, 'ACA': academic, 'FAC': Facilities
buildingsDict = [{'label': 'Antero Apartments', 'value': 'ANT', 'type': 'RES'},
                 {'label': 'Armstrong Hall', 'value': 'ARM', 'type': 'ACA'},
                 {'label': 'Arthur House', 'value': 'ART', 'type': 'RES'},
                 {'label': 'Bemis Hall', 'value': 'BEM', 'type': 'RES'},
                 {'label': 'Blanca Apartments', 'value': 'BLA', 'type': 'RES'},
                 {'label': 'Boettcher Center', 'value': 'BOE', 'type': 'FAC'},
                 {'label': 'Colorado Springs Fine Arts Center', 'value': 'FAC', 'type': 'FAC'},
                 {'label': 'Cutler Hall', 'value': 'CUT', 'type': 'ACA'},
                 {'label': 'East Campus Apartments', 'value': 'EAS', 'type': 'RES'},
                 {'label': 'Edith Gaylord House', 'value': 'GAY', 'type': 'RES'},
                 {'label': 'Edith Kinney Gaylord Cornerstone Arts Center', 'value': 'CNR', 'type': 'ACA'},
                 {'label': 'El Diente Apartments', 'value': 'ELD', 'type': 'RES'},
                 {'label': 'El Pomar Sports Center', 'value': 'POM', 'type': 'FAC'},
                 {'label': 'Honnen Ice Arena', 'value': 'HON', 'type': 'FAC'},
                 {'label': 'Lloyd E. Worner Campus Center', 'value': 'WOR', 'type': 'FAC'},
                 {'label': 'John Lord Knight Apartments', 'value': 'JLK', 'type': 'RES'},
                 {'label': 'Loomis Hall', 'value': 'LOO', 'type': 'RES'},
                 {'label': 'Matthias Hall', 'value': 'MAT', 'type': 'RES'},
                 {'label': 'McGregor Hall', 'value': 'MCG', 'type': 'RES'},
                 {'label': 'Montgomery Hall', 'value': 'MON', 'type': 'RES'},
                 {'label': 'Olin Hall', 'value': 'OLI', 'type': 'ACA'},
                 {'label': 'Palmer Hall', 'value': 'PAL', 'type': 'ACA'},
                 {'label': 'Russell T. Tutt Science Center', 'value': 'TUT', 'type': 'ACA'},
                 {'label': 'Shove Memorial Chapel', 'value': 'SHC', 'type': 'FAC'},
                 {'label': 'South Hall', 'value': 'SOU', 'type': 'RES'},
                 {'label': 'Sperry S. and Ella Graber Packard Hall of Music and Art', 'value': 'PAC', 'type': 'ACA'},
                 {'label': 'Ticknor Hall', 'value': 'TIC', 'type': 'RES'},
                 {'label': 'Tutt Library', 'value': 'TLB', 'type': 'ACA'},
                 {'label': 'William I. Spencer Center', 'value': 'SPE', 'type': 'ACA'}]

dataTypeDict = [{'label': 'Carbon', 'value': 'CARB'},
                {'label': 'Energy', 'value': 'ENER'},
                {'label': 'Electricity', 'value': 'ELEC'},
                {'label': 'Heat', 'value': 'HEAT'}]

intervalOptions = [{'label': 'Cumulative', 'value': 'CUM'},
                     {'label': '15 Minute', 'value': 'MIN'},
                     #{'label': 'Hourly', 'value': 'HOU'},
                     #{'label': 'Weekly', 'value': 'WEE'},
                     #{'label': 'Day of Week', 'value': 'DOW'},
                     #{'label': 'Quarterly', 'value': 'QUA'},
                     #{'label': 'Monthly', 'value': 'MON'},
                     #{'label': 'Annually', 'value': 'ANN'},
                     {'label': 'Daily', 'value': 'DAY'}]

ELECGraphLabels = {'title': 'Net Electricity',
                   'xaxis': 'Time',
                   'yaxis': 'kWh'}

HEATGraphLabels = {'title': 'Net Heat',
                   'xaxis': 'Time',
                   'yaxis': 'kBTU'}

CARBGraphLabels = {'title': 'Net Carbon',
                   'xaxis': 'Time',
                   'yaxis': 'Metric Tons of Carbon'}

ENERGraphLabels = {'title': 'Net Energy',
                   'xaxis': 'Time',
                   'yaxis': 'kWh'}

tuttDashboardTables = ['ARM', 'TLB', 'TUT', 'OLI', 'PAL']

def getGraphLabelsDictForType(type):
    if type == 'ELEC':
        return ELECGraphLabels
    elif type == 'HEAT':
        return HEATGraphLabels
    elif type == 'CARB':
        return CARBGraphLabels
    elif type == 'ENER':
        return ENERGraphLabels

def getNameFromValue(value):
    for building in buildingsDict:
        if building['value'] == value:
            return building['label']

def getTypeFromTypeValue(value):
    for typ in dataTypeDict:
        if typ['value'] == value:
            return typ['label']

def getTablesForValue(value):
    tables = []
    for table in tablesDict:
        if table['value'] is value:
            tables.append(table)
    return tables

def getTypesForDataType(dataType, value):
    dataTypes = []
    if dataType == 'HEAT':
        dataTypes.append(dataType)
    elif dataType == 'ELEC':
        dataTypes.append(dataType)
    elif (dataType == 'ENER') or (dataType == 'CARB'):
        dataTypes.append('ELEC')
        dataTypes.append('HEAT')
        if value == 'TLB':
            dataTypes.append('NGAS')
    return dataTypes

def getTablesWithTypeForValue(dataType, value):
    tables = []
    types = []
    for type in getTypesForDataType(dataType, value):
        for table in tablesDict:
            if table['type'] == type and table['value'] == value:
                tables.append(table['name'])
                types.append(table['type'])
    return {'tables': tables, 'types': types}

def hasType(tables, type):
    for table in tables:
        if table['type'] == type:
            return True
    return False

def canGenerateGraphWithType(value, type):
    tables = getTablesForValue(value)
    if type == 'ELEC' or type == 'HEAT':
        return hasType(tables, type)
    elif type == 'ENER' or type == 'CARB':
        return hasType(tables, 'ELEC') and hasType(tables, 'HEAT')

# type = HEAT ELEC CARB ENER
def getBuildingsWithGraphType(type='CARB'):
    compatibleBuildings = []
    for building in buildingsDict:
       if canGenerateGraphWithType(building['value'], type):
            compatibleBuildings.append(building)
    return compatibleBuildings
