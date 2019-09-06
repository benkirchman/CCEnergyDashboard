import datetime
import dash
import dash_core_components as dcc
import plotly.graph_objs as go

def getMultiGraph(dataframes,
                  names,
                  idString,
                  yaxisLabel,
                  xaxisLabel,
                  cumulative = True,
                  showButtons = True,
                  rangeValue = 25,
                  showTimeSlider = True,
                  width = 1500,
                  height = 1000,
                  minX = datetime.datetime(2018,1,1)):
    scatters = []
    r = 208
    g = 155
    b = 44
    if showButtons is True:
        buttonsListDict = dict(buttons = list([
            dict(count=1,
                label='1d',
                step='day',
                stepmode='backward'),
            dict(count=7,
                label='1w',
                step='day',
                stepmode='backward'),
            dict(count=1,
                label='1m',
                step='month',
                stepmode='backward'),
            dict(count=6,
                label='6m',
                step='month',
                stepmode='backward'),
            dict(count=1,
                label='YTD',
                step='year',
                stepmode='todate'),
            dict(count=1,
                label='1y',
                step='year',
                stepmode='backward'),
            dict(step='all')
        ]))
    else:
        buttonsListDict = None
    for dataframe, frameName in zip(dataframes, names):
        scatter = go.Scatter(
            visible = True,
            x = dataframe['timeStamp'],
            y = (dataframe['value'].cumsum() if cumulative else dataframe['value']),
            line = dict(
                #color = ('rgb(242,112,89)')
                color = ('rgba(' + str(r) + ',' + str(g) + ',' + str(b) + ', 0.75)')
            ),
            name = frameName
        )
        # Just some random numbers
        r = (r + 181) % 250
        g = (g + 97) % 250
        b = (b + 29) % 250
        scatters.append(scatter)

    return dcc.Graph(
        id=idString,
        figure=go.Figure(
            data=scatters,
            layout=go.Layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=700,
                autosize=True,
                title=idString,
                xaxis=dict(title=xaxisLabel,
                    zeroline=True,
                    zerolinecolor='#C95327',
                    zerolinewidth=8,
                    rangeselector=buttonsListDict,
                    range=[minX, datetime.date.today()],
                    type='date'
                ),
                yaxis = (dict(title=yaxisLabel)),# if cumulative else dict(title=yaxisLabel, range=[0,rangeValue])),
            )
        ),
        config={'displaylogo':False}
    )
