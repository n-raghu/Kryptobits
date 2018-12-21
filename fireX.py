while(True):
	from xcalc import *
	nuXch=[]
	xchData=[]
	xlist=popForex()
	xchDataDicts=list(cnxCH.find())
	invokeDB=False
	if len(xchDataDicts)==0:
		for x in xlist:
			writeFullXch(x)

	for _ in xchDataDicts:
		idi=_['_id']
		xchData.append(idi)
		_r=_['rates']
		if(len(_r)<100):
			nuXch.append(idi)
	nuXch.append(set(xlist)-set(xchData))
	nuXch=list(set(nuXch))

	for x_x in nuXch:
		writeFullXch(x_x,prd=True)

	ziz(9600)