from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
from flask_cors import CORS, cross_origin

db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)

CORS(app)

class Customers(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from customers")
        result = {'customers': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class Customers_byId(Resource):
    def get(self, customer_id):
        conn = db_connect.connect()
        query = conn.execute("select * from customers where CustomerId =%d "  %int(customer_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)


class Customers_Delete(Resource):
        @app.route("/customers_delete/<customer_id>", methods = ["post"])
        def delete(customer_id):
            conn = db_connect.connect()
            query = conn.execute("delete from customers where CustomerId = %d" %int(customer_id))
            return "iihhhh"

class Customers_Name_Update(Resource):
	def post(self, customer_id):
		conn = db_connect.connect()
		newName = request.data
		sql = "update customers set FirstName=? where CustomerId = ?"
		conn.execute(sql,(newName,customer_id))
		
api.add_resource(Customers, '/customers')
api.add_resource(Customers_byId, '/customers/<customer_id>')
#api.add_resource(Customers_Delete,'/customers_delete/<customer_id>')
api.add_resource(Customers_Name_Update,'/customers_update/<customer_id>')



if __name__ == '__main__':
     app.run(port='5002')
