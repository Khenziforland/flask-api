from flask import Flask
from db import db
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db.init_app(app)
api = Api(app)

from Models.User import UserModel

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
        
        # Periksa apakah username sudah ada
        existing_username = UserModel.query.filter_by(username=args['username']).first()
        if existing_username:
            abort(400, message="Username sudah digunakan")
        
        # Periksa apakah email sudah ada
        existing_email = UserModel.query.filter_by(email=args['email']).first()
        if existing_email:
            abort(400, message="Email sudah digunakan")
        
        user = UserModel(username=args['username'], email=args['email'], password=args['password'])
        db.session.add(user)
        db.session.commit()
        return user, 201

# * Update Data
class UpdateData(Resource):
    @marshal_with(userFields)
    def put(self, id):
        args = user_args.parse_args()

        # Periksa ID
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User tidak ditemukan")
        
        # Periksa apakah username baru sudah digunakan oleh pengguna lain
        existing_username = UserModel.query.filter(UserModel.username == args['username'], UserModel.id != id).first()
        if existing_username:
            abort(400, message="Username sudah digunakan oleh pengguna lain")
        
        # Periksa apakah email baru sudah digunakan oleh pengguna lain
        existing_email = UserModel.query.filter(UserModel.email == args['email'], UserModel.id != id).first()
        if existing_email:
            abort(400, message="Email sudah digunakan oleh pengguna lain")
        
        # Perbarui Data
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