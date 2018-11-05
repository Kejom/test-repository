import os

from flask import Flask
from flask_restful import  Api
from resources import Page, Pages, AddPage, PagesInit, UserRegister, AdminInit
from flask_jwt import JWT
from security import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Ilikepie'
api = Api(app)

from db import db
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  #/auth

#checks the page with coresponding id and returns result - no auth required
api.add_resource(Page, '/page/<string:id>')
# checks and returns all pages from db with results - no auth required
api.add_resource(Pages, '/pages')
# Post and Delete - allows to add or remove page from db - requires JWT auth
api.add_resource(AddPage, '/page')
# sets up database with all required pages - requires JWT auth
api.add_resource(PagesInit,'/pages/init')  # sets up database with all required pages - requires JWT auth
# Registers new user - required json with "username" and "password" - JWT auth required
api.add_resource(UserRegister, '/register')
# sets up admin account during first run
api.add_resource(AdminInit, '/admininit')



if __name__ == '__main__':
    app.run()
