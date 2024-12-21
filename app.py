from flask import Flask
from src.routes import initialize_routes
from src.interactor.Database.sql_alchemy import setup_sqlalchemy
from src.Repository.token_repository import TokenRepository
import os
from flask_session import Session
from datetime import timedelta
# from flask_oauthlib.provider import OAuth2Provider

from authlib.integrations.flask_client import OAuth
app = Flask(__name__,template_folder='src/frontend')

app.secret_key = 'my_secret_key2' 
app.config['SESSION_TYPE'] = 'filesystem' 
app.config.from_object(__name__)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
app.permanent_session_lifetime = timedelta(minutes=120)
REDIRECT_URI = 'https://9f93-14-139-105-18.ngrok-free.app/oauth/callback'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SWAGGER_UI_JSONEDITOR'] = True
setup_sqlalchemy(app)
# TokenRepository.initialize_database(app)
initialize_routes(app)
Session(app)

if __name__ == '__main__':
    app.run(debug=True)
