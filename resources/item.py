from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from model.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help="Name of product, cannot be empty!"
    )
    parser.add_argument('category',
        type=str,
        required=False,
        help="Category of product, can be defoult - other!"
    )
    parser.add_argument('unit',
        type=str,
        required=True,
        help="unit, required"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name, category, unit):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = ItemModel.parser.parse_args()

        item = ItemModel(name,**data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occure inserting the item."}, 500
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name, category, unit):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
              
        if item is None:
           item = ItemModel(name, **data)
        else:
           item.category = data['category']
           item.unit = data['unit']

        item.save_to_db()

        return item.json


class ItemList(Resource):
    def get(self):
       return {'items': [item.json() for item in ItemModel.query.all()]} 