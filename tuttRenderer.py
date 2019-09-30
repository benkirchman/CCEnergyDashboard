import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_reusable_components as drc
import localDB
import datetime
import dataUtil
import renderer
import plotly.graph_objs as go
import statistics

coalFactor = 4008

def getGraph(dataframes,
                  names,
                  idString,
                  yaxisLabel,
                  xaxisLabel,
                  cumulative = True,
                  showButtons = True,
                  rangeValue = 25,
                  showTimeSlider = True,
                  minX = datetime.datetime(2018,1,1)):
    scatters = []
    colors = []
    r = 208
    g = 155
    b = 44
    colors.append(('rgba(' + str(r) + ',' + str(g) + ',' + str(b) + ', 0.75)'))
    buttonsListDict = None
    for dataframe, frameName in zip(dataframes, names):
        dataframe = dataframe
        scatter = go.Scatter(
            visible = True,
            x = dataframe['timeStamp'],
            y = dataframe['value'].cumsum(),
            line = dict(
                #color = ('rgb(242,112,89)')
                color = colors[-1]
                ),
            name = frameName
        )
        colors.append(('rgba(' + str(r) + ',' + str(g) + ',' + str(b) + ', 0.75)'))
        # Just some random numbers
        r = (r + 121) % 250
        g = (g + 80) % 250
        b = (b + 29) % 250
        scatters.append(scatter)

    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=700,
        width = 1000,
        title=idString,
        xaxis=dict(
            title=xaxisLabel,
            zeroline=True,
            zerolinecolor='#C95327',
            zerolinewidth=8,
            rangeselector=buttonsListDict,
            range=[minX, datetime.date.today()],
            type='date',
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickcolor='rgb(204, 204, 204)',
            tickwidth=2,
            ticklen=5,
            tickfont=dict(
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            title=yaxisLabel,
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        autosize=True,
        margin=dict(
            autoexpand=True,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=False
    )

    annotations = []
    # Adding labels
    #for y_trace, label, color in zip(y_data, labels, colors):
    for dataframe, frameName, color in zip(dataframes, names, colors):

        # labeling the right_side of the plot
        annotations.append(dict(xref='paper', x=1, y=dataframe['value'].cumsum().iloc[-1],
                                xanchor='right', yanchor='middle',
                                text=frameName + ' {}'.format('%.1f'%(dataframe['value'].cumsum().iloc[-1])),
                                font=dict(size=16, color='#000000'),
                                bgcolor=color,
                                arrowhead=2,
                                arrowsize=1,
                                arrowwidth=2,
                                arrowcolor='#636363',
                                ax=-30,
                                ay=-10,
                                opacity=0.8,
                                showarrow=True))

    layout['annotations'] = annotations


    return dcc.Graph(
        id=idString,
        figure=go.Figure(
            data=scatters,
            layout=layout
        ),
        config={'displaylogo':False}
    )


def getTuttText(tuttCarb, otherCarbs):
    meanCarb = statistics.mean(otherCarbs)
    percentCarb = str(int((1-(tuttCarb/meanCarb)) * 100))
    tuttCarbString = ' {}'.format('%.1f'%(tuttCarb))
    tuttSavings = int(meanCarb - tuttCarb)
    tuttSavingsInCoal = "{:,}".format(int(tuttSavings * coalFactor))
    s = "Tutt Library has produced " + tuttCarbString + " metric tons of carbon "
    s += "in the past week. That is " + percentCarb + "% less than the average "
    s += "for academic buildings at CC!"
    s2 = "Tutt Library saved " + str(tuttSavings) + " metric tons of carbon "
    s2 += "over other academic buildings at CC. This is equivalent to "
    s2 += tuttSavingsInCoal + " pounds of coal not being burned!"
    return (s, s2)

def getTuttGraph():
        tables = localDB.tuttDashboardTables
        oneWeekAgo = datetime.datetime.now() - datetime.timedelta(days = 7)
        dataType = 'CARB'
        serieses = []
        labels = []
        tuttCarb = 0
        otherCarbs = []
        for value in tables:
            #Check if we must perfrom special behavior for Tutt Library dataset
            dataframes = []
            result = localDB.getTablesWithTypeForValue(dataType, value)
            if result:
                for table, type in zip(result['tables'], result['types']):
                    df = dataUtil.getDFWithCache(table, dataType, type, minDate = oneWeekAgo)
                    dataframes.append(df)
            series = dataUtil.sumDataframes(dataframes)
            if series is not None:
                carbon = series['value'].cumsum().iloc[-1]
                if value is 'TLB':
                    tuttCarb = carbon
                else:
                    otherCarbs.append(carbon)
                serieses.append(series)
            name = localDB.getNameFromValue(value)
            labels.append(name)
        labelsDict = localDB.getGraphLabelsDictForType(dataType)

        return (getGraph(serieses,
                          labels,
                          idString = "Net Carbon Emissions By Academic Buildings",
                          yaxisLabel = labelsDict['yaxis'],
                          xaxisLabel = labelsDict['xaxis'],
                          cumulative = True,
                          showButtons = False,
                          minX = oneWeekAgo), getTuttText(tuttCarb, otherCarbs))

def getTuttPage():
    (graph, text) = getTuttGraph()
    string1, string2 = text
    return html.Div([
        html.Div(className="banner", children=[
            # Change App Name here
            html.Div(className='container scalable', children=[
                # Change App Name here
                html.Img(src="https://www.coloradocollege.edu/offices/sustainability/resources/CC_OOS_WhitePlain_Diagonal.png",
                        style={
                            'max-width': '30%',
                            'display': 'inline-block',
                            'float': 'left',

                        },
                ),
                html.H1(
                    'Carbon Snapshot',
                    style={
                        'text-decoration': 'none',
                        'color': 'inherit',
                        'max-width': '50%',
                        'margin': 'auto',
                        'display': 'inline-block',
                        'float': 'right'
                    }
                ),
            ], style={'margin': '20px'}),
        ]),
        html.Div([
            #Columns
            html.Div([
                drc.Card([
                    html.H4(
                        string1
                    ),
                    html.H4(
                        string2
                    )
                ]),
                html.H5(
                    "For more information visit the Office of Sustainability website at: www.coloradocollege.edu/offices/sustainability"
                ),
                html.Img(src="https://www.coloradocollege.edu/offices/sustainability/resources/OOS_qr_code.png"
                ),
                ], className="one-third column", style={'max-height': '75%'}),
            html.Div([
                drc.Card(id='graph_card', children=
                     html.Div(children=[graph])),
                ], className="two-thirds column", style={'max-height': '75%'}),

        ], className="row")
    ], style={'margin': '5%', 'width': '1610px', 'height': '907px'})
