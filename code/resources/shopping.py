from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from model.shopping import ShoppingModel

class Shopping(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help="Name of product, cannot be empty!"
    )
    parser.add_argument('status',
        type=str,
        required=False,
        help="Statuses: toBuy, bougth, cancel"
    )

    @jwt_required()
    def get(self, name):
        shopping = ShoppingModel.find_by_name(name)
        if shopping:
            return shopping.json()
        return {'message': 'Shopping list not found'}, 404

    def post(self, name, category, unit):
        if ShoppingModel.find_by_name(name):
            return {'message': "An Shopping list with name '{}' already exists.".format(name)}

        data = ShoppingModel.parser.parse_args()

        shopping = ShoppingModel(name,**data)

        try:
            ShoppingModel.save_to_db()
        except:
            return {"message": "An error occure inserting the shopping list."}, 500
        return shopping.json(), 201

    @jwt_required()
    def delete(self, name):
        shopping = ShoppingModel.find_by_name(name)
        if shopping:
            shopping.delete_from_db()

        return {'message': 'Shopping list deleted'}

    @jwt_required()
    def put(self, name, items, unit):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
              
        if item is None:
           item = ItemModel(name, **data)
        else:
           item.category = data['category']
           item.unit = data['unit']

        item.save_to_db()

        return item.json


class ShoppingList(Resource):
    def get(self):
       return {'items': [shopping.json() for shopping in ShoppingModel.query.all()]} 