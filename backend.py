# using flask_restful
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from tinydb import TinyDB, Query

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)

db = TinyDB('db.json')

# get all items on grocery list
class Index(Resource):

	def get(self):

		return db.all(), 200


# add item to grocery list
class Add(Resource):

    def get(self, item):
        db.insert({"item": item})
        return {'success': "added item to list"}, 200

# remove item from grocery list
class Remove(Resource):
	
    def get(self, item):

        if (item=="*"):
            db.truncate()
            return {"success": "all items removed from list"}
        
        items = Query()
        if len(db.search(items.item==item)) == 0:
              return {"failure": "item not in list"}
        
        db.remove(items.item==item)
        return {"success": "item removed from list"}

# adding the defined resources along with their corresponding urls
api.add_resource(Index, '/')
api.add_resource(Add, '/add/<string:item>')
api.add_resource(Remove, '/remove/<string:item>')


# driver function
if __name__ == '__main__':

	app.run(debug = True)
