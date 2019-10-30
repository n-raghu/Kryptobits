import sqlalchemy as say
from yaml import safe_load
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime as dtm
from sqlalchemy.dialects.postgresql import UUID

BASE = declarative_base()

with open('app.yml', 'r') as yFile:
    cfg = safe_load(yFile)

DT = say.Date
TXT = say.Text
COL = say.Column
STR = say.String
FLOAT = say.Float
NUM = say.NUMERIC
INT = say.Integer
TABLE = say.Table
BOOL = say.Boolean
BIGINT = say.BIGINT
LBY = say.LargeBinary
TIMES = say.TIMESTAMP


class Keys(BASE):
    __tablename__ = 'rsakeys_v1'
    active = COL(BOOL)
    deprecated = COL(BOOL)
    key_id = COL(TXT)
    pub_key = COL(LBY)
    pvt_key = COL(LBY)
    time_created = COL(TIMES)
    last_mod_stamp = COL(TIMES)
    deprecation_stamp = COL(TIMES)
    tbl_id = COL(UUID(as_uuid=True), primary_key=True)


class KeyRequester(BASE):
    __tablename__ = 'key_requester_events'
    key_id = COL(TXT)
    requester = COL(TXT)
    request_stamp = COL(TIMES)
    tbl_id = COL(UUID(as_uuid=True), primary_key=True)


class ErrorLogs(BASE):
    __tablename__ = 'errorlogs'
    err_class = COL(STR)
    err_resource = COL(STR)
    err_msg = COL(STR)
    app_stamp = COL(TIMES)
    db_stamp = COL(TIMES, server_default=say.sql.text('CURRENT_TIMESTAMP'))
    tbl_id = COL(UUID(as_uuid=True), primary_key=True)


if __name__ == '__main__':
    from yaml import safe_load
    urx = 'postgresql://' +cfg['datastore']['uid']+ ':' +cfg['datastore']['pwd']+ '@' +cfg['datastore']['host']+ ':' +str(cfg['datastore']['port'])+ '/' +cfg['datastore']['db']
    pge = say.create_engine(urx)
    BASE.metadata.create_all(pge)
    pge.dispose()
