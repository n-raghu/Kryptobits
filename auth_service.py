from flask import Flask
from flask_restful import Api
from cryptography.fernet import Fernet
from flask_jwt_extended import JWTManager

from auth_resources import cfg, GenNewToken

app=Flask(__name__)
fnt_instance = Fernet(cfg['key']['global_key'].encode())
app.config['JWT_SECRET_KEY'] = fnt_instance.decrypt(cfg['key']['jwt_key'].encode()).decode()
fnt_instance = False
jwt = JWTManager(app)
api = Api(app)

api.add_resource(GenNewToken,'/auth/v1/login')

app.run(
        debug=cfg['auth']['debug'],
        host=cfg['auth']['host'],
        port=cfg['auth']['port']
)