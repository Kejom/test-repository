from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models import PageModel, UserModel
from multiprocessing import Pool
from checkmethod import pagescheck

class Page(Resource):


    def get(self, id):
        page = PageModel.find_by_id(id)
        if page:
            return {"result": pagescheck([page.id, page.url])}
        return {'message': "page with id {} doesnt exist".format(id)}, 404


class AddPage(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('url', type=str, required=True, help="url required")

    @jwt_required()
    def post(self):
        request_data = AddPage.parser.parse_args()
        if PageModel.find_by_url(request_data['url']):
            return {"message": "Page already exists in database"},400
        page = PageModel(request_data['url'])
        try:
            page.save_to_db()
        except:
            return {"message": "An error occured"},500
        return {"message": "page added"}


    @jwt_required()
    def delete(self):
        request_data = AddPage.parser.parse_args()
        page = PageModel.find_by_url(request_data['url'])
        if page:
            page.delete_from_db()
            return {"message": "page {} deleted from db".format(request_data['url'])}
        return {"message": "error - page {} doesnt exist in db".format(request_data['url'])}

class Pages(Resource):
    def get(self):
        pages = PageModel.query.all()
        urls = [[page.id, page.url] for page in pages]
        pool = Pool()
        return {"results": pool.map(pagescheck, urls)}

class PagesInit(Resource):
    def post(self):
        pages = open("pages.txt","r")
        for line in pages:
            page = PageModel(line.strip("\n"))
            page.save_to_db()
        return {"message": "database updated"}








class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank!")

    @jwt_required()
    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created succesfully."}, 201



class AdminInit(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank!")

    def post(self):
        data = AdminInit.parser.parse_args()
        if data['username'] == '1337' and data['password'] == '1337':
            admin = UserModel("admin", "ILikePie")
            admin.save_to_db()
            return {"message": "Admin setup completed"},201
        return {"Error": "404"},404
