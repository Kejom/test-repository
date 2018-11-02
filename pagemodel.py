from db import db


class PageModel(db.Model):

    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)

    def __init__(self, url):
        self.url = url

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_url(cls, url):
        return cls.query.filter_by(url=url).first()



