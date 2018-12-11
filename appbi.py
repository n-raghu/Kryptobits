from tcalc import *

x_css=['https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css']
server=Flask(__name__)
appBI=dash.Dash(__name__,external_stylesheets=x_css,server=server)

ndqList=yfi.tickers_nasdaq()
snpList=yfi.tickers_sp500()
fexList=popForex()
all_options=ndqList+snpList
gblDict=odict([('tickr',getNAQticker('pfg')['Price']),('xch',getXchVal('INR')),('shares',100)])

appBI.layout=htm.Div(
    htm.Div([
        htm.Div([htm.H3(children='Hello!, We make analytics speak ',className='nine columns')],className="row"),
        htm.Div([
                htm.Div([
                        htm.Div(dcc.Markdown('''**Ticker** '''),className='three columns'),
                        htm.Div(htm.P(''),className='one column'),
                        htm.Div(dcc.Markdown('''**Popular Currecies** '''),className='two columns'),
                        htm.Div(htm.P(''),className='one column'),
                        htm.Div(dcc.Markdown('''**Shares you've** '''),className='three columns'),
                        htm.Div(dcc.Dropdown(options=[{'label': i, 'value': i} for i in all_options],value="PFG",id='allTicks'),className='three columns'),
                        htm.Div(htm.P(''),className='one column'),
                        htm.Div(dcc.Dropdown(options=[{'label': i, 'value': i} for i in fexList],value="INR",id='xCH'),className='two columns'),
                        htm.Div(htm.P(''),className='one column'),
                        htm.Div(dcc.Input(id='xcalc',type='text',value=100,className='three columns')),
                        ],style={'margin-top':'10'}
                )
            ],className="row"),
        htm.Div([
            htm.Div(id='tkrBox',className='three columns'),
            htm.Div(htm.P(''),className='one column'),
            htm.Div(id='xchBox',className='two columns'),
            htm.Div(htm.P(''),className='one column'),
            htm.Div(id='shrBox',className='four columns')
            ],className="row")
    ],className='ten columns offset-by-one')
)

@appBI.callback(Output('tkrBox','children'),[Input('allTicks','value')])
def refresh_stocks(tickr):
    global gblDict
    tkr=getNAQticker(tickr,3)
    gblDict['tickr']=tkr['Price']
    htDiv=[htm.H5('Share Price: ' +str(tkr['Price']))]
    return htDiv

@appBI.callback(Output('xchBox','children'),[Input('xCH','value')])
def refresh_currency(cnc):
    global gblDict
    cnc=getXchVal(cnc,3)
    gblDict['xch']=cnc
    return [htm.H5('Exchange: ' +str(cnc))]

@appBI.callback(Output('shrBox','children'),[Input('xcalc','value')])
def refresh_share(shares):
    global gblDict
    gblDict['shares']=int(shares)
    bookVal=round(gblDict['xch']*gblDict['tickr']*int(shares),3)
    return [htm.H5(str(bookVal))]

if __name__=='__main__':
    appBI.run_server(debug=True,host='0.0.0.0',port=8888)
