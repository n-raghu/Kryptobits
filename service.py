from flask import Flask
from flask_restful import Api
from cryptography.fernet import Fernet
from flask_jwt_extended import JWTManager

from resources import cfg, PubKey, PvtKey

app = Flask(__name__)
fnt_instance = Fernet(cfg['key']['global_key'].encode())
app.config['JWT_SECRET_KEY'] = fnt_instance.decrypt(cfg['key']['jwt_key'].encode()).decode()
fnt_instance = False
jwt = JWTManager(app)
api = Api(app)

api.add_resource(PubKey, '/krs/v1/pubkey')
api.add_resource(PvtKey, '/krs/v1/pvtkey')

app.run(
        debug=cfg['app']['debug'],
        host=cfg['app']['host'],
        port=cfg['app']['port']
)