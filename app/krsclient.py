import json
import base64
import requests as req

from yaml import safe_load
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key

with open('app.yml', 'r') as yml_file:
    cfg = safe_load(yml_file)
api_public = cfg['krs']['pub_key']
api_private = cfg['krs']['pvt_key']
api_head = {'Content-Type': 'app/json'}

def encipher(msg, use_old_pub_key=False, rsa=True):
    key = Fernet.generate_key()
    fernet_instance = Fernet(key)
    msg_en = fernet_instance.encrypt(msg)
    if rsa:
        if use_old_pub_key:
            pub_key = use_old_pub_key
        else:
            pub_key_response = req.get(api_public, headers=api_head)
            pub_key = json.loads(pub_key_response.text)
        pub_key_instance = load_pem_public_key( pub_key['pub_key'].encode(), backend=default_backend() )
        cipher_text = pub_key_instance.encrypt(
                key,
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        return json.dumps( {'msg':msg_en.decode(), 'msg_key':base64.b64encode(cipher_text).decode(), 'krs_key':pub_key['key_id']} ).encode()

def crypt_asymmetric(msg):
    return None

def decipher(msg, auth_token):
    dat = json.loads(msg)
    dat['krs_key']
    dataHeadR = {'Content-Type':'application/json', 'Authorization':'Bearer {}'.format(auth_token)}
    pvt_res = req.get(url=api_private, json={'key_id': dat['krs_key']}, headers=dataHeadR).json()
    pvt_key = pvt_res['pvt_key'].encode()
    pvt_key_instance = load_pem_private_key( pvt_key, password=None, backend=default_backend() )
    msg_key_rsa = base64.b64decode(dat['msg_key'])
    msg_key = pvt_key_instance.decrypt(
                msg_key_rsa,
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    pvt_key_instance = None
    pvt_key = None
    pvt_res = None
    fnt = Fernet(msg_key)
    return fnt.decrypt( dat['msg'].encode() )

def decrypt_asymmetric(msg):
    return None
