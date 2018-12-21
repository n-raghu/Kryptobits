from adsLib import *
from time import mktime,sleep as ziz

ccc=cccodes()
connexion=mcx(dbConStr)
today=dtm.utcnow()
xlist=popForex()
cnxCH=connexion['ads']['xchange']

def scrapeXchSet(currency,ndays=5):
	doc=odict()
	if(currency in xlist):
		i=-1
		rates=[]
		while(i<=ndays):
			day=today-timedelta(abs(i))
			tmpVal=ccr.get_rate('USD',currency,day)
			stamp=mktime(today.timetuple())
			rates.append({'day':day,'cost':tmpVal,'recorded':today,'stamp':stamp})
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

def writeFullXch(cnc,prd=False):
	if(prd):
		xdays=dtm.utcnow()-dtm(2016,1,1,1,1,1,111)
		xdays=xdays.days
	else:
		xdays=5
	xdict=scrapeXchSet(cnc,ndays=xdays)
	if(xdict):
		odo=cnxCH.update_one({'_id':xdict['_id']},xdict,upsert=True)
	else:
		odo=False
	return odo

def pushNewXch():
	oldSet=list(cnxCH.find())
	bucket=cnxCH.initialize_unordered_bulk_op()
	todayRates=[]
	for currency in xlist:
		todayRates.append(scrapeXchSet(currency,-1))
	for rate in todayRates:
		bucket.find({'_id':rate['_id']},{'$push':{'rates':rate['rates'][0]}})
	return bucket.execute()
