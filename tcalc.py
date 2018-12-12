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

xlist=popForex()

def getXchSet(currency,ndays=188,rnum=3):
	fullSet=odict()
	if(currency in xlist):
		today=dtm.utcnow().date()
		i=0
		while(i<ndays):
			day=today-timedelta(i)
			fullSet[day]=round(ccr.get_rate('USD',currency,day),rnum)
			i+=1
	else:
		fullSet=False
	return fullSet