from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User username={self.username}, email={self.email}, password={self.password}>'

user_args = reqparse.RequestParser()
user_args.add_argument("username", type=str, help="Username is required", required=True)
user_args.add_argument("email", type=str, help="Email is required", required=True)
user_args.add_argument("password", type=str, help="Password is required", required=True)

userFields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'password': fields.String
}

# * Get Data
class GetData(Resource):
    @marshal_with(userFields)
    def get(self):
        user = UserModel.query.all()
        return user
    
# * Detail Data
class DetailData(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        return user
            
# * Create Data
class CreateData(Resource):
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(username=args['username'], email=args['email'], password=args['password'])
        db.session.add(user)
        db.session.commit()
        return user, 201

# * Update Data
class UpdateData(Resource):
    @marshal_with(userFields)
    def put(self, id):
        args = user_args.parse_args()

        # Check ID
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        
        # Update Data
        user.username = args['username']
        user.email = args['email']
        user.password = args['password']
        db.session.commit()
        return user
    
    # * Delete Data
class DeleteData(Resource):
    def delete(self, id):
        user = UserModel.query.get(id)
        if not user:
            return {"Message": "ID User Tidak Ditemukan"}, 404
        try:
            db.session.delete(user)
            db.session.commit()
            return {"Message": "Data User Berhasil Dihapus"}, 200
        except:
            db.session.rollback()
            return {"Message": "Gagal Menghapus Data User"}, 500


api.add_resource(GetData, "/api/users/")
api.add_resource(DetailData, "/api/users/<int:id>")
api.add_resource(CreateData, "/api/users/")
api.add_resource(UpdateData, "/api/users/<int:id>")
api.add_resource(DeleteData, "/api/users/<int:id>")

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