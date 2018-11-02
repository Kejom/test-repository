from flask_restful import Resource, reqparse
from pagemodel import PageModel
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
        return ("database updated")



