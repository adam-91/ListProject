from db import db
from model.item import ItemModel

class ShopListModel(db.Model):
    __tablename__ = 'shop_list'

    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'))
    item_id = db.Column(db.Integer)
    value = db.Column(db.Float(2))
    status = db.Column(db.String(40))

    def __init__(self, list_id, item, value, status):
        self.list_id = list_id
        self.item_id = item
        self.value = value
        self.status = status

    def json(self):
        return {'name': ListsModel.find_by_id(self.list_id), 'item': ItemModel.find_by_id(self.item_id), 'value': self.value, 'status': self.status}

    @classmethod
    def find_by_item(cls, item_id):
        return cls.query.filter_by(item_id=item_id).all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_list_id(cls, list_id):
        return cls.query.filter_by(list_id=list_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
