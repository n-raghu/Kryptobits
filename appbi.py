from tcalc import *

x_css=['https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css']
server=Flask(__name__)
appBI=dash.Dash(__name__,external_stylesheets=x_css,server=server)

ndqList=yfi.tickers_nasdaq()
snpList=yfi.tickers_sp500()
fexList=popForex()
all_options=ndqList+snpList
gblDict=odict([('tickr',getNAQticker('pfg')['Price']),('shares',100),('xch',71)])
xchSet=odict()

appBI.layout=htm.Div(
	htm.Div([
		htm.Div([htm.H3(children='Hello!, Visualizing Analytics',className='nine columns')],className="row"),
		htm.Div([
			htm.Div([
				htm.Div(dcc.Markdown(''' **Ticker**'''),className='three columns'),
				htm.Div(htm.P(''),className='one column'),
				htm.Div(dcc.Markdown(''' **Popular Currecies**'''),className='two columns'),
				htm.Div(htm.P(''),className='one column'),
				htm.Div(dcc.Markdown(''' **Shares you've**'''),className='three columns'),
				htm.Div(dcc.Dropdown(options=[{'label': i, 'value': i} for i in all_options],value="PFG",id='allTicks'),className='three columns'),
				htm.Div(htm.P(''),className='one column'),
				htm.Div(dcc.Dropdown(options=[{'label': i, 'value': i} for i in fexList],value="INR",id='xCH'),className='two columns'),
				htm.Div(htm.P(''),className='one column'),
				htm.Div(dcc.Input(id='xcalc',type='number',value=100,className='two columns')),
				],style={'margin-top':'10'}
				)],className="row"),
		htm.Div([
			htm.Div(id='tkrBox',className='three columns'),
			htm.Div(htm.P(''),className='one column'),
			htm.Div(id='xchBox',className='two columns'),
			htm.Div(htm.P(''),className='one column'),
			htm.Div(id='shrBox',className='three columns')
			],className="row"),
		htm.Div([dcc.Graph(id='tkrGraph',className='eleven columns')],className='row'),
		htm.Div([dcc.Graph(id='xchGraph',className='eleven columns')],className='row'),
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
	today=dtm.utcnow().date()
	if cnc in xchSet:
		xchSet[cnc][today]=round(ccr.get_rate('USD',cnc),3)
	else:
		xSet=getXchSet(cnc,ndays=7)
		if(xSet):
			print('Add ' +cnc+ ' to dictiionary.')
			xchSet[cnc]=xSet
	gblDict['xch']=xchSet[cnc][today]
	return [htm.H5(' ~' +str(gblDict['xch']))]

@appBI.callback(Output('shrBox','children'),[Input('xcalc','value')])
def refresh_share(shares):
	global gblDict
	today=dtm.utcnow().date()
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
	if cnc in xchSet:
		dfo=pdf(data={'dtt':list(xchSet[cnc].keys()),'prc':list(xchSet[cnc].values())})
		trace={'x':dfo.dtt,'y':dfo.prc}
	else:
		trace={'x':[1,2,],'y':[2,1]}
	return { 'data':[trace],'layout':{'title':'Exchange Trends'} }

if __name__=='__main__':
	appBI.run_server(debug=True,host='0.0.0.0',port=8888)