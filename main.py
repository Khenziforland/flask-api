from flask import Flask
from db import db
from flask_restful import Api, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db.init_app(app)
api = Api(app)

from Controllers.UserController import GetData, DetailData, CreateData, UpdateData, DeleteData


api.add_resource(GetData, "/api/users/")
api.add_resource(DetailData, "/api/users/<string:id>")
api.add_resource(CreateData, "/api/users/")
api.add_resource(UpdateData, "/api/users/<string:id>")
api.add_resource(DeleteData, "/api/users/<string:id>")

resource_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'password': fields.String
}
@app.route('/')
def home():
    return '<h1>Hello World</h1>'

if __name__ == '__main__':
    app.run(debug=True)