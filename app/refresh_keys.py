from datetime import datetime as dtm
from uuid import uuid4 as UU4, uuid1 as UU1

from flask_restful import Resource
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine as dbeng

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.fernet import Fernet, MultiFernet as MFT
from cryptography.hazmat.primitives.asymmetric import padding

from model import Keys as K
from resources import cfg, urx, dataSession

def gen_key(mkey, gkey, akey, ksize):
	unlock_set = [Fernet(akey.encode()), Fernet(gkey.encode())]
	mft = MFT(unlock_set)
	pvt_key=rsa.generate_private_key(
		public_exponent=65537,
		key_size=ksize,
		backend=default_backend()
	)
	pvt_pem=pvt_key.private_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PrivateFormat.PKCS8,
		encryption_algorithm=serialization.BestAvailableEncryption(mft.decrypt(mkey.encode()))
	)
	pub_key=pvt_key.public_key()
	pub_pem=pub_key.public_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PublicFormat.SubjectPublicKeyInfo
	)

	return {'pub_key': pub_pem, 'pvt_key': pvt_pem, 'key_id': UU4().hex}

key_store=[]
key_size = int(cfg['key']['key_size'])
master_key = cfg['key']['master_key']
global_key = cfg['key']['global_key']
app_key = 'rH_wkQVjM3ub6LOD1qGNA8fff12cIvljEDwWtKj-VNw='

for _ in range(1,10):
	rsa_doc=gen_key(master_key, global_key, app_key, key_size)
	rsa_doc['tbl_id'] = UU1()
	rsa_doc['active'] = True
	rsa_doc['deprecated'] = False
	rsa_doc['time_created'] = dtm.utcnow()
	rsa_doc['last_mod_stamp'] = dtm.utcnow()
	key_store.append(K(**rsa_doc))

eventSession=dataSession(urx)
eventSession.add_all(key_store)
eventSession.commit()
eventSession.close()