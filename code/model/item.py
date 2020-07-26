from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    category = db.Column(db.String(80))
    value = db.Column(db.Float(2))
    unit = db.Column(db.String(3))

    def __init__(self, name, category, value, unit):
        self.name = name
        self.category = category
        self.value = value
        self.unit = unit

    def json(self):
        return {'name': self.name, 'category': self.category, 'value': self.value, 'unit': self.unit}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
