from adsLib import *

ccr=ccrates()

def popForex():
	flist=list(ccr.get_rates('USD',dtm.utcnow()).keys())
	flist.append('USD')
	return flist

def getNAQticker(tkr,rnum=5):
	if(tkr==None):
		tkrData=odict([('Ticker',tkr),('Price',0)])
	else:
		tkrcost=round(yfi.get_live_price(tkr),rnum)
		tkrData=odict([('Ticker',tkr),('Price',tkrcost)])
	return tkrData

def getXchVal(currency,rnum=5):
	if(currency):
		cnc=currency
	else:
		cnc='USD'
	return round(ccr.get_rate('USD',cnc),rnum)
