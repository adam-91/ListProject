from app import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    category = db.Column(db.String(80))
    unit = db.Column(db.String(1))

    def __init__(self, name, category, unit):
        self.name = name
        self.category = category
        self.unit = unit

    def json(self):
        return {'name': self.name, 'category': self.category, 'unit': self.unit}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()