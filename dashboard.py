import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_reusable_components as drc
import localDB
import renderer
import tuttRenderer
import numpy
import dataUtil

app = dash.Dash()
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

dashboard_layout = html.Div([
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
                'Energy Dashboard',
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
                drc.NamedRadioItems(
                    name='Data Type',
                    id='data-type-radio',
                    options=localDB.dataTypeDict,
                    value=localDB.dataTypeDict[2]['value'],
                ),
                drc.NamedDropdown(
                    name='Sources (max 5)',
                    id='dataset-dropdown',
                    options=localDB.buildingsDict,
                    clearable=False,
                    searchable=True,
                    multi=True,
                ),
                drc.NamedRadioItems(
                    name='Interval',
                    id='data-interval-radio',
                    options=localDB.intervalOptions,
                    value=localDB.intervalOptions[2]['value'],
                ),
                html.Button('Update', id='update-button')
            ])
            ], className="one-third column"),

        drc.Card([html.Div(id='graph')], className="two-thirds column"),
    ], className="row")
], style={'margin': '5%'})

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/carbon':
        return tuttRenderer.getTuttPage()
    else:
        return dashboard_layout

@app.callback(
    dash.dependencies.Output('graph', 'children'),
     #n_clicks unused
    [dash.dependencies.Input('update-button', 'n_clicks')],
    [dash.dependencies.State('data-type-radio', 'value'),
     dash.dependencies.State('dataset-dropdown', 'value'),
     dash.dependencies.State('data-interval-radio', 'value')  ]
)
def update_dataset_dropdown(n_clicks, dataType, tableValues, intervalValue):
    finalDfs = []
    labels = []
    if(len(tableValues) > 5):
        tableValues = tableValues[:5]
    isCumulative = intervalValue == 'CUM'
    for value in tableValues:
        #Check if we must perfrom special behavior for Tutt Library dataset
        dataframes = []
        result = localDB.getTablesWithTypeForValue(dataType, value)
        if result:
            for table, type in zip(result['tables'], result['types']):
                df = dataUtil.getDFWithCache(table, dataType, type)
                dataframes.append(df)
        summedDF = dataUtil.sumDataframes(dataframes)
        if summedDF is not None:
            summedDF = dataUtil.getDFSum(summedDF, intervalValue)
            finalDfs.append(summedDF)
        name = localDB.getNameFromValue(value)
        labels.append(name)
    labelsDict = localDB.getGraphLabelsDictForType(dataType)
    return renderer.getMultiGraph(finalDfs,
                                  labels,
                                  idString = labelsDict['title'],
                                  yaxisLabel = labelsDict['yaxis'],
                                  xaxisLabel = labelsDict['xaxis'],
                                  cumulative = isCumulative)
external_css = ["https://codepen.io/chriddyp/pen/brPBPO.css",
                "https://www.coloradocollege.edu/global/css/2017/bootstrap.min.css",
                'https://codepen.io/b_kirchman_cc/pen/QPOqOR.css',
                "https://fonts.googleapis.com/css?family=Crimson+Text:400,400i,700,700i|Montserrat:300,300i,700,700i"]
for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(debug=False)
