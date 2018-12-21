import os,socket as soc
from collections import OrderedDict as odict
from datetime import datetime as dtm,timedelta
from pandas import DataFrame as pdf,read_sql
from pandas_datareader import data as pdr
from yahoo_fin import stock_info as yfi
from forex_python.converter import CurrencyRates as ccrates,CurrencyCodes as cccodes
from pymongo import MongoClient as mcx
from flask import Flask
from time import mktime

dbConStr=soc.gethostbyname(soc.gethostname()) +':36069'
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

def getXchSet():
	pipe=[{'$unwind':'$rates'},	{'$project':{'day':'$rates.day','cost':'$rates.cost','_id':0,'idx':'$_id'}}]
	connexion=mcx(dbConStr)
	aggSet=connexion['ads']['xchange'].aggregate(pipe)
	dfo=pdf(list(aggSet))
	connexion.close()
	dfo['day']=dfo['day'].dt.strftime('%d-%b-%y')
	dfo.set_index(['idx','day'],inplace=True,drop=False)
	return dfo

def refreshXchSet(cnc=False):
	nList=[]
	if(cnc):
		nList.append(odict([('cost',ccr.get_rate('USD',cnc)),('day','Now'),('idx',cnc)]))
	else:
		flist=list(ccr.get_rates('USD',dtm.utcnow()).keys())
		for cnc in flist:
			nList.append(odict([('cost',ccr.get_rate('USD',cnc)),('day','Now'),('idx',cnc)]))
	frame=pdf(nList)
	frame.set_index(['idx','day'],inplace=True,drop=False)
	return frame

def xchCodes():
	connexion=mcx(dbConStr)
	pipe=[{'$project':{'code':{'$concat':['$currency',' - ','$code']},'_id':0,'currency':'$_id'}}]
	codes=connexion['ads']['xchange'].aggregate(pipe)
	connexion.close()
	return codes