from adsLib import *

def getNAQticker(tkr,currency=False,rnum=5):
	tkrcost=round(yfi.get_live_price(tkr),rnum)
	tkrData=odict([('tickr',tkr),('Price',tkrcost),('UnitPrice',tkrcost)])
	if(currency):
		ccr=ccrates()
		xrate=round(ccr.get_rate('USD',currency),rnum)
		tkrData['Exchange']=xrate
		tkrData['UnitPrice']=round(xrate*tkrcost,rnum)
	return tkrData
