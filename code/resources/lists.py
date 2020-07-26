from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from model.lists import ListModel
from model.shopList import ShopListModel

class Lists(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help="Name of list, cannot be empty!"
    )
    parser.add_argument('list_type',
        type=str,
        required=True,
        help="List type: shopList or toDoList"
    )
  
    @jwt_required()
    def get(self, name):
        _list = ListModel.find_by_name(name)
        if _list:
            return _list.json()
        return {'message': 'List not found'}, 404

    def post(self, name, category, unit):
        if ListModel.find_by_name(name):
            return {'message': "A list with name '{}' already exists.".format(name)}

        data = ListModel.parser.parse_args()

        _list = ListModel(name,**data)

        try:
            _list.save_to_db()
        except:
            return {"message": "An error occure inserting the list."}, 500
        return _list.json(), 201

    @jwt_required()
    def delete(self, name):
        _list = ListModel.find_by_name(name)
        if _list:
            #usunąć wszystkie rekordy odwołujące się do tej listy z list zakupów
            _list.delete_from_db()

        return {'message': 'List deleted'}

    @jwt_required()
    def put(self, name, category, unit):
        data = List.parser.parse_args()

        _list = ListModel.find_by_name(name)
              
        if _list is None:
           _list = ListModel(name, **data)
        else:
           _list.category = data['category']
           _list.unit = data['unit']

        _list.save_to_db()

        return _list.json


class ListsList(Resource):
    def get(self):
       return {'items': [_list.json() for _list in ListModel.query.all()]} 