from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_sqlalchemy import SQLAlchemy
from db import db

#from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.shopping import Shopping, ShoppingList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'test'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

#jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Shopping, '/shopping/<string:name>')
api.add_resource(ShoppingList, '/shoppings')

if __name__ == '__main__':
    
    db.init_app(app)
    app.run(debug=True)  
      