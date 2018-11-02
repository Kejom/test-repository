from flask import Flask
from flask_restful import  Api
from pageresource import Page, Pages, AddPage, PagesInit



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Ilikepie'
api = Api(app)

from db import db
db.init_app(app)

api.add_resource(Page, '/page/<string:id>')
api.add_resource(Pages, '/pages')
api.add_resource(AddPage, '/page/add')
api.add_resource(PagesInit,'/pages/init')





app.run()
