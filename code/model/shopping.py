from db import db
from model.item import ItemModel

class ShoppingModel(db.Model):
    __tablename__ = 'shopping'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique = True)
    items = db.relationship('ItemModel', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(40))

    def __init__(self, name, item, user_id, status):
        self.name = name
        self.items = items
        self.user_id = user_id
        self.status = status

    def json(self):
        return {'name': self.name, 'items': self.items, 'status': self.status, 'user': UserModel.search_by_id(user_id)}

    #@classmethod
    #def find_by_item(cls, item):
    #    return cls.query.filter_by(item=item).all()

    @classmethod
    def find_by_id(cls, _id):
         return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
