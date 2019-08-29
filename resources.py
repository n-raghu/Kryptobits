import random
from uuid import uuid4 as UU4
from datetime import datetime as dtm
from time import perf_counter as tpc

from yaml import safe_load
from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine as dbeng
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet, MultiFernet as MFT
from flask_jwt_extended import jwt_required, get_jwt_identity

from model import Keys as K, KeyRequester as KR

with open('app.yml', 'r') as yFile:
	cfg=safe_load(yFile)

urx = 'postgresql://' +cfg['datastore']['uid']+ ':' +cfg['datastore']['pwd']+ '@' +cfg['datastore']['host']+ ':' +str(cfg['datastore']['port'])+ '/' +cfg['datastore']['db']

now = tpc()
pub_key_store = []
pvt_key_store = []
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

class KeyStore(Resource):
	def get(self):
		return jsonify(random.choice(pub_key_store))

class PvtKey(Resource):
	@jwt_required
	def get(self):
		if not request.json:
			return jsonify('Invalid')
		else:
			k_id = request.json.get('key_id', None)
			key_json = next(i for i in pvt_key_store if i['key_id'] == k_id )
			key_json['requester'] = get_jwt_identity()
			record_key_request(key_json['key_id'], key_json['requester'])
			return jsonify(key_json)