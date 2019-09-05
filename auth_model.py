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

class User(BASE):
	__tablename__ = 'users'
	uid = COL(TXT,primary_key=True)
	pwd = COL(TXT)
	user_name = COL(TXT)
	roleid = COL(INT)

class UserRole(BASE):
	__tablename__ = 'userroles'
	rid = COL(INT,primary_key=True)
	rolename = COL(TXT)
	tokentime = COL(INT)

if __name__=='__main__':
	from yaml import safe_load
	urx = 'postgresql://' +cfg['datastore']['uid']+ ':' +cfg['datastore']['pwd']+ '@' +cfg['datastore']['host']+ ':' +str(cfg['datastore']['port'])+ '/' +cfg['datastore']['db']
	pge=say.create_engine(urx)
	BASE.metadata.create_all(pge)
	pge.dispose()
