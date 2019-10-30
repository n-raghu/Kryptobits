import sys
from flask import Flask
from flask_restful import Api
from cryptography.fernet import Fernet
from flask_jwt_extended import JWTManager

from resources import urx, cfg, PubKey, PvtKey, record_error


try:
    app_host = cfg['app']['host']
    app_port = cfg['app']['port']
    app_debug = cfg['app']['debug']
    fnt_instance = Fernet(cfg['key']['global_key'].encode())
    app.config['JWT_SECRET_KEY'] = fnt_instance.decrypt(cfg['key']['jwt_key'].encode()).decode()
except Exception as err:
    record_error(
        urx,
        e_class='service',
        e_rsrc='import-app-config',
        e_msg=str(err)
    )
    sys.exit(1)

try:
    app = Flask(__name__)
    fnt_instance = False
    jwt = JWTManager(app)
    api = Api(app)
except Exception as err:
    record_error(
        urx,
        e_class='service',
        e_rsrc='configure-service',
        e_msg=str(err)
    )
    sys.exit(1)

try:
    api.add_resource(PubKey, '/krs/v1/pubkey')
    api.add_resource(PvtKey, '/krs/v1/pvtkey')
except Exception as err:
    record_error(
        urx,
        e_class='service',
        e_rsrc='configure-resources',
        e_msg=str(err)
    )
    sys.exit(1)

try:
    app.run(
        debug=app_debug,
        host=app_host,
        port=app_port,
    )
except Exception as err:
    record_error(
        urx,
        e_class='service',
        e_rsrc='run',
        e_msg=str(err)
    )
    sys.exit(1)
