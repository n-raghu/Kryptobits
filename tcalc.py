from adsLib import *

ccc=cccodes()
connexion=mcx(dbConStr)
today=dtm.utcnow()
xlist=popForex()

def scrapeXchSet(currency,ndays=188):
	doc=odict()
	if(currency in xlist):
		i=-1
		rates=[]
		while(i<=ndays):
			day=today-timedelta(abs(i))
			tmpVal=ccr.get_rate('USD',currency,day)
			rates.append({'day':day,'cost':tmpVal,'recorded':today})
			if(i==0):
				i+=1
			i+=1
		doc['rates']=rates
		doc['_id']=currency
		doc['code']=ccc.get_symbol(currency)
		doc['currency']=ccc.get_currency_name(currency)
	else:
		doc=False
	return doc

def writeNewXch(onecnc=False):
	odo=False
	lox=[]
	xdays=dtm.utcnow()-dtm(2016,1,1,1,1,1,111)
	if(onecnc):
		xdict=scrapeXchSet(onecnc,ndays=5)
		if(xdict):
			lox.append(xdict)
		else:
			lox=False
	else:
		for xxc in xlist:
			xdict=scrapeXchSet(xxc,ndays=2)
			if(xdict):
				lox.append(xdict)
			else:
				lox=False
	if(lox):
		odo=connexion['ads']['xchange'].insert_many(lox)
	return odo

def writeOldXch():
	oldSet=list(connexion['ads']['xchange'].find())
	todayRates=[]
	for currency in xlist:
		todayRates.append(scrapeXchSet(currency,-1))
	return todayRates