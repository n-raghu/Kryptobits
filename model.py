import sqlalchemy as say
from yaml import safe_load
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime as dtm
from sqlalchemy.dialects.postgresql import UUID

BASE=declarative_base()

with open('app.yml', 'r') as yFile:
	cfg=safe_load(yFile)

COL=say.Column
INT=say.Integer
BOOL=say.Boolean
BIGINT=say.BIGINT
FLOAT=say.Float
TABLE=say.Table
STR=say.String
TXT=say.Text
TIMES=say.TIMESTAMP
DT=say.Date
NUM=say.NUMERIC
LBY=say.LargeBinary

class Keys(BASE):
	__tablename__='rsakeys_v1'
	active=COL(BOOL)
	deprecated=COL(BOOL)
	key_id=COL(TXT)
	pub_key=COL(LBY)
	pvt_key=COL(LBY)
	time_created=COL(TIMES)
	last_mod_stamp=COL(TIMES)
	deprecation_stamp=COL(TIMES)
	tbl_id=COL(UUID(as_uuid=True), primary_key=True)

class KeyRequester(BASE):
	__tablename__ = 'key_requester_events'
	key_id=COL(TXT)
	requester=COL(TXT)
	request_stamp=COL(TIMES)
	tbl_id=COL(UUID(as_uuid=True), primary_key=True)

if __name__=='__main__':
	from yaml import safe_load
	urx = 'postgresql://' +cfg['datastore']['uid']+ ':' +cfg['datastore']['pwd']+ '@' +cfg['datastore']['host']+ ':' +str(cfg['datastore']['port'])+ '/' +cfg['datastore']['db']
	pge=say.create_engine(urx)
	BASE.metadata.create_all(pge)
	pge.dispose()
