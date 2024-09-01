from flask_restful import Resource, reqparse, fields, marshal_with, abort
from Models.User import UserModel
from db import db

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