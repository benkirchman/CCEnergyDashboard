import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_reusable_components as drc
import localDB
import renderer
import tuttRenderer
import numpy
import dataUtil
import csv
import tempfile
import os
import flask
import pandas as pd
import xlsxwriter

app = dash.Dash()
# Bug: https://github.com/plotly/dash/issues/802
app.css.config.serve_locally = False
server = app.server
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
                html.Button('Update', id='update-button'),
                html.A(
                        'Download Data',
                        id='download-link',
                        href='',
                        style={'display':'block'}
                    )
            ])
            ], className="one-third column"),

        drc.Card([html.Div(id='graph')], className="two-thirds column"),
    ], className="row"),
], style={'margin': '5%'})

@app.callback(
    dash.dependencies.Output('download-link', 'href'),
    [dash.dependencies.Input('data-type-radio', 'value'),
     dash.dependencies.Input('dataset-dropdown', 'value'),
     dash.dependencies.Input('data-interval-radio', 'value')  ]
)
def setDownlodLink(dataType, tableValues, intervalValue):
    buildingValue = tableValues[0]
    return '/API/' + buildingValue + '/' + dataType + '/' + 'EXCEL'

#API
@server.route('/API/<string:building>/<string:type>/<string:format>')
@server.route('/api/<string:building>/<string:type>/<string:format>')
def serveAPI(building, type, format):
    format = format.upper()
    type = type.upper()
    building = building.upper()
    dataframe = getDataFrame(building, type)
    return getResponse(building, type, format, dataframe)

def getResponse(building, type, format, dataframe):
    with tempfile.TemporaryDirectory() as tmpdirname:
        name = localDB.getNameFromValue(building) + "_" + localDB.getTypeFromTypeValue(type)
        tmpName = "Temp Dir Path"
        if format == "HTML":
            return dataframe.to_html()
        elif format == "CSV":
            name = name + ".csv"
            tmpName = os.path.join(tmpdirname, name)
            dataframe.to_csv(tmpName)
        elif format == "EXCEL":
            name = name + ".xlsx"
            tmpName = os.path.join(tmpdirname, name)
            dataframe.to_excel(tmpName, index=False)
        elif format == "JSON":
            name = name + ".json"
            tmpName = os.path.join(tmpdirname, name)
            dataframe.to_json(tmpName, orient='records')
        else:
            return "Error: API Command not recognized"
        response = flask.send_file(tmpName, as_attachment=True, attachment_filename=name)
        response.headers["filename"] = name
        response.headers["Access-Control-Expose-Headers"] = 'filename'
        return response

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
        summedDF = getDataFrame(value, dataType)
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

def getDataFrame(value, dataType):
    dataframes = []
    result = localDB.getTablesWithTypeForValue(dataType, value)
    if result:
        for table, type in zip(result['tables'], result['types']):
            df = dataUtil.getDFWithCache(table, dataType, type)
            dataframes.append(df)
    return dataUtil.sumDataframes(dataframes)



external_css = ["https://codepen.io/chriddyp/pen/brPBPO.css",
                "https://www.coloradocollege.edu/global/css/2017/bootstrap.min.css",
                'https://codepen.io/b_kirchman_cc/pen/QPOqOR.css',
                "https://fonts.googleapis.com/css?family=Crimson+Text:400,400i,700,700i|Montserrat:300,300i,700,700i"]
for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(debug=False)
