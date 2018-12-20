from adsLib import *

ccc=cccodes()
connexion=mcx(dbConStr)
today=dtm.utcnow()
xlist=popForex()
cnxCH=connexion['ads']['xchange']

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

def writeFullXch(onecnc=False,devqa=False):
	odo=False
	lox=[]
	if(devqa):
		xdays=5
	else:
		xdays=dtm.utcnow()-dtm(2016,1,1,1,1,1,111)
		xdays=xdays.days
	if(onecnc):
		xdict=scrapeXchSet(onecnc,ndays=xdays)
		if(xdict):
			lox.append(xdict)
		else:
			lox=False
	else:
		for xxc in xlist:
			xdict=scrapeXchSet(xxc,ndays=xdays)
			if(xdict):
				lox.append(xdict)
			else:
				lox=False
	if(lox):
		odo=cnxCH.insert_many(lox)
	return odo

def writeNewXch():
	oldSet=list(cnxCH.find())
	bucket=cnxCH.initialize_unordered_bulk_op()
	todayRates=[]
	for currency in xlist:
		todayRates.append(scrapeXchSet(currency,-1))
	for rate in todayRates:
		bucket.find({'_id':rate['_id']},{'$push':{'rates':rate['rates'][0]}})
	return bucket.execute()