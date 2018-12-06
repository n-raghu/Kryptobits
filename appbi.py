from tcalc import *

x_css=['https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css']
server=Flask(__name__)
appBI=dash.Dash(__name__,external_stylesheets=x_css,server=server)

usaList=['New York City','San Francisco','Cincinnati']
canList=[u'Montreal','Toronto','Ottawa']
all_options={'US':usaList,'Canada':canList,'All':usaList+canList}

city_data={
    'San Francisco': {'x': [1, 2, 3], 'y': [4, 1, 2]},
    'Montreal': {'x': [1, 2, 3], 'y': [2, 4, 5]},
    'New York City': {'x': [1, 2, 3], 'y': [2, 2, 7]},
    'Cincinnati': {'x': [1, 2, 3], 'y': [1, 0, 2]},
    'Toronto': {'x': [1, 2, 3], 'y': [4, 7, 3]},
    'Ottawa': {'x': [1, 2, 3], 'y': [2, 3, 3]}
}

tbl=getNAQticker('pfg','INR')

appBI.layout=htm.Div(
    htm.Div([
        htm.Div([
                htm.H1(children='Hello!!!',className='nine columns'),
                htm.Div([dcc.Markdown(''' *Making analytics speak* ''')],className='nine columns')
            ],className="row"),

        htm.Div([
                htm.Div([
                        dcc.Markdown(''' **Country** '''),
                        dcc.RadioItems(id='Country',
                                options=[{'label': k,'value': k} for k in all_options.keys()],
                                value='All',labelStyle={'display':'inline-block'}),
                    ],
                    className='twelve columns',
                    style={'margin-top': '10'}
                ),
                htm.Div([
                        dcc.Markdown(''' **Select Cities** '''),
                        dcc.Dropdown(options=[
                            {'label': 'New York City', 'value': 'NYC'},
                            {'label': 'Montréal', 'value': 'MTL'},
                            {'label': 'San Francisco', 'value': 'SF'}
                            ],multi=True,value="MTL",id='Cities'
                        )],
                    className='six columns',style={'margin-top':'10'}
                )
            ],className="row"),

        htm.Div([
            htm.Div([dcc.Graph(id='barGraph')], className='six columns'),
            htm.Div(htm.P(''),className='one column'),
            htm.Div([
                htm.H3('Share Price: ' +str(tbl['Price'])),
                htm.H3('Exchange: ' +str(tbl['Exchange'])),
                htm.H3('100 Shares: ' +str(100*tbl['UnitPrice']))
                ],className='five columns')
        ],className="row")
    ],className='ten columns offset-by-one')
)

@appBI.callback(
    dash.dependencies.Output('Cities','options'),
    [dash.dependencies.Input('Country', 'value')])
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]

@appBI.callback(
    dash.dependencies.Output('barGraph','figure'),
    [dash.dependencies.Input('Cities','value')])
def update_image_src(selector):
    data=[]
    for city in selector:
        data.append({'x':city_data[city]['x'],'y':city_data[city]['y'],'type':'bar','name':city})
    figure={'data':data,'layout':{'title':'Graph Representation'}}
    return figure

if __name__=='__main__':
    appBI.run_server(debug=True,host='0.0.0.0')