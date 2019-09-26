import random
import asyncio as aio
from uuid import uuid4 as UU4
from datetime import datetime as dtm

from yaml import safe_load
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine as dbeng
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet, MultiFernet as MFT

from model import Keys as K, KeyRequester as KR, cfg


from fastapi import FastAPI
from pydantic import BaseModel

urx = 'postgresql://' +cfg['datastore']['uid']+ ':' +cfg['datastore']['pwd']+ '@' +cfg['datastore']['host']+ ':' +str(cfg['datastore']['port'])+ '/' +cfg['datastore']['db']

pub_key_store = []
pvt_key_store = []
KAFKA = cfg['kafka']['enable']
master_key = cfg['key']['master_key']
global_key = cfg['key']['global_key']
key_size = int(cfg['key']['key_size'])
app_key = 'rH_wkQVjM3ub6LOD1qGNA8fff12cIvljEDwWtKj-VNw='

def dataSession(urx):
	pgx = dbeng(urx)
	SessionClass = sessionmaker(bind=pgx)
	Session = SessionClass()
	return Session

def record_key_request(key_id, requester):
	event_session = dataSession(urx)
	event_doc = { 'key_id': key_id, 'requester': requester, 'request_stamp': dtm.utcnow(), 'tbl_id': UU4() }
	event_session.add(KR(**event_doc))
	event_session.commit()
	return None

event_session = dataSession(urx)
pub_key_store_en = event_session.query(K).filter(K.active==True).with_entities(K.key_id, K.pub_key).all()
event_session.close()
event_session = dataSession(urx)
pvt_key_store_en = event_session.query(K).filter(K.deprecated==False).with_entities(K.key_id, K.pvt_key).all()
event_session = dataSession(urx)
unlock_set = [Fernet(app_key.encode()), Fernet(global_key.encode())]
mft = MFT(unlock_set)

for _ in pvt_key_store_en:
	_tup_ = {'key_id': _[0]}
	_pvt_ = serialization.load_pem_private_key(
			_[1],
			password=mft.decrypt(master_key.encode()),
			backend=default_backend()
		)
	_pem_ =_pvt_.private_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PrivateFormat.PKCS8,
		encryption_algorithm=serialization.NoEncryption()
	).decode()
	_tup_['pvt_key'] = _pem_
	pvt_key_store.append(_tup_)

pvt_key_store_en.clear()

for _ in pub_key_store_en:
	_tup_ = {
		'key_id'  : _[0],
		'pub_key' : _[1].decode(),
		}
	pub_key_store.append(_tup_)

if KAFKA:
	P = Producer({'bootstrap.servers': cfg['kafka']['host']})

pvt_key_gen = (_ for _ in pvt_key_store)

pub_key_point = '/krs/v1/pub_key'
pvt_key_point = '/krs/v1/pvt_key'

class KeyDoc(BaseModel):
	key_id: str
	pvt_key: int = 8

async def key_private(kid):
	for keypair in pvt_key_store:
		if keypair['key_id'] == kid:
			print(keypair)
			return keypair
	return {kid: 'Private Key not Found'}

async def private_task(kid, loop):
	print('Got Task')
	task = loop.create_task(key_private(kid))
	return await aio.wait([task])

app = FastAPI()

@app.get(pub_key_point)
async def get_pub():
	return random.choice(pub_key_store)

@app.get(pvt_key_point)
async def get_pvt(key_doc: KeyDoc):
	kid = key_doc.key_id
	try:
		loop = aio.get_event_loop()
		kpair = loop.run_until_complete( private_task(kid, loop) )
	except Exception as err:
		print(err)
	return kpair

@app.get("/")
async def root():
	return {"message": "AIO"}