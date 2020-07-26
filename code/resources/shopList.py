from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from model.shopList import ShopListModel

class ShopList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('list_id',
        type=int,
        required=True,
        help="List id from Lists!"
    )
    parser.add_argument('item_id',
        type=int,
        required=True,
        help="Item id from Item"
    )
    parser.add_argument('value',
        type=float,
        required=True,
        help="value, required"
    )
    parser.add_argument('status',
        type=str,
        required=True,
        help="Statuses: toBuy, purchased, partialBuy; required parameter"
    )

    @jwt_required()
    def get(self, _id):
        shopList = ShopListModel.find_by_id(_id)
        if shopList:
            return shopList.json()
        return {'message': 'Shopping list not found'}, 404

    def post(self, list_id, item_id, value,status):
        if ShopListModel.find_by_id(list_id):
            return {'message': "A shopping list with id '{}' already exists.".format(list_id)}

        data = ShopListModel.parser.parse_args()

        shopList = ShopListModel(name,**data)

        try:
            shopList.save_to_db()
        except:
            return {"message": "An error occure inserting the shopping list."}, 500
        return shopList.json(), 201

    @jwt_required()
    def delete(self, name):
        shopList = ShopListModel.find_by_name(name)
        if shopList:
            shopList.delete_from_db()

        return {'message': 'Shopping list deleted'}

    @jwt_required()
    def put(self, list_id, item_id, value, status):
        data = shopList.parser.parse_args()

        shopList = ShopListModel.find_by_name(name)
              
        if shopList is None:
           shopList = ShopListModel(name, **data)
        else:
           shopList.list_id = data['list_id']
           shopList.item_id = data['item_id']
           shopList.value = data['value']
           shopList.status = data['status']

        shopList.save_to_db()

        return shopList.json


class ItemList(Resource):
    def get(self):
       return {'items': [shopList.json() for shopList in ShopListModel.query.all()]} 