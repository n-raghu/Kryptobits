from adsLib import *
import dash,dash_core_components as dcc,dash_html_components as htm,dash_table as dtl
from dash.dependencies import Input, Output
from plotly import graph_objs as go

x_css=['https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css']
server=Flask(__name__)
appBI=dash.Dash(__name__,external_stylesheets=x_css,server=server)

fexList=list(xchCodes())
tkrList=yfi.tickers_nasdaq()+yfi.tickers_sp500()
gblDict=odict([('tickr',getNAQticker('pfg')['Price']),('shares',100),('xch',ccr.get_rate('USD','INR'))])
xchSet=getXchSet().append(refreshXchSet())
classVol=odict([('graph','ten columns'),('tkr','three columns'),('cnc','three columns'),('shares','three columns'),('r1_spc','one column')])

appBI.layout=htm.Div(
	htm.Div([
		htm.Div([htm.H3(children='Hello!, Visualizing Analytics',className='nine columns')],className="row"),
		htm.Div([
			htm.Div([
				htm.Div(dcc.Markdown(''' **Ticker**'''),className=classVol['tkr']),
				htm.Div(htm.P(''),className=classVol['r1_spc']),
				htm.Div(dcc.Markdown(''' **Popular Currecies**'''),className=classVol['cnc']),
				htm.Div(htm.P(''),className=classVol['r1_spc']),
				htm.Div(dcc.Markdown(''' **Shares you've**'''),className=classVol['shares']),
				htm.Div(dcc.Dropdown(options=[{'label':i, 'value':i} for i in tkrList],value="PFG",id='allTicks'),className=classVol['tkr']),
				htm.Div(htm.P(''),className=classVol['r1_spc']),
				htm.Div(dcc.Dropdown(options=[{'label':i['code'], 'value':i['currency']} for i in fexList],value="INR",id='xCH'),className=classVol['cnc']),
				htm.Div(htm.P(''),className=classVol['r1_spc']),
				htm.Div(dcc.Input(id='xcalc',type='number',value=100,className=classVol['shares'])),
				],style={'margin-top':'10'}
				)],className="row"),
		htm.Div([
			htm.Div(id='tkrBox',className=classVol['tkr']),
			htm.Div(htm.P(''),className=classVol['r1_spc']),
			htm.Div(id='xchBox',className=classVol['cnc']),
			htm.Div(htm.P(''),className=classVol['r1_spc']),
			htm.Div(id='shrBox',className=classVol['shares'])
			],className="row"),
		htm.Div([dcc.Graph(id='tkrGraph',className=classVol['graph'])],className='row'),
		htm.Div([dcc.Graph(id='xchGraph',className=classVol['graph'])],className='row'),
		],className='ten columns offset-by-one'
))

@appBI.callback(Output('tkrBox','children'),[Input('allTicks','value')])
def refresh_stocks(tickr):
	global gblDict
	tkr=getNAQticker(tickr,3)
	gblDict['tickr']=tkr['Price']
	htDiv=[htm.H5(' $' +str(tkr['Price']))]
	return htDiv

@appBI.callback(Output('xchBox','children'),[Input('xCH','value')])
def refresh_currency(cnc):
	global gblDict,xchSet
	xchSet.update(getXchSet())
	xchSet.update(refreshXchSet(cnc))
	gblDict['xch']=xchSet.loc[cnc,'Now']['cost']
	return [htm.H5(' ~' +str(xchSet.loc[cnc,'Now']['cost']))]

@appBI.callback(Output('shrBox','children'),[Input('xcalc','value')])
def refresh_share(shares):
	global gblDict
	gblDict['shares']=shares
	bookVal=round(gblDict['xch']*gblDict['tickr']*gblDict['shares'],3)
	return [htm.H5(bookVal)]

@appBI.callback(Output('tkrGraph','figure'),[Input('allTicks','value')])
def refresh_tkrTrend(tkr):
	start=dtm.utcnow()
	tFrame=pdr.DataReader(tkr,'iex',start-timedelta(188),start)
	trace=go.Ohlc(x=list(tFrame.index),open=tFrame['open'],high=tFrame['high'],low=tFrame['low'],close=tFrame['close'])
	figure={'data':[trace],'layout':{'title': 'Stock Trends'}}
	return figure

@appBI.callback(Output('xchGraph','figure'),[Input('xCH','value')])
def refresh_xchTrend(cnc):
	global xchSet
	if cnc in xchSet.index:
		trace={'x':xchSet.loc[cnc]['day'],'y':xchSet.loc[cnc]['cost']}
	else:
		trace={'x':[1,2,],'y':[2,1]}
	return { 'data':[trace],'layout':{'title':'Exchange Trends'} }

if __name__=='__main__':
	appBI.run_server(debug=True,host='0.0.0.0',port=8888)