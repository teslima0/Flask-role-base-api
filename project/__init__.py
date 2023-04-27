from flask import Flask
from flask_jwt_extended import JWTManager,get_jwt_identity
import os
from config import settings
from flask_cors import CORS
from flask_migrate import Migrate
#from flask_jwt_extended.exceptions import JWTDecodeError
from flask_sqlalchemy import SQLAlchemy
app= Flask(__name__)

db = SQLAlchemy()


jwt = JWTManager(app)
def create_app(config_name="development"):
    #app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_DATABASE_URI']=os.getenv("DATABASE_URI")
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    #CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    
    app.config.from_object(settings[config_name])
    
    db.init_app(app)
    jwt.init_app(app)
    #migrate = Migrate(app, db)
   
    #from .import models

    


    #register view
    from .authentication.auth import auths
    #from .auths import auths

    app.register_blueprint(auths, url_prefix='/')
    #app.register_blueprint(deletes, url_prefix='/')
    #app.register_blueprint(auths, url_prefix='/')

    return app

from .models import CustomUser



@jwt.user_identity_loader
def user_identity_lookup(customuser):
    return customuser.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_payload):
    identity = jwt_payload["sub"]
    return CustomUser.query.filter_by(id=identity).one_or_none()

