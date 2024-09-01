from flask_restful import Resource, reqparse, fields, marshal_with, abort
from Models.ProductCategory import ProductCategoryModel
from db import db

productCategory_args = reqparse.RequestParser()
productCategory_args.add_argument("name", type=str, help="Name is required", required=True)
productCategory_args.add_argument("description", type=str, help="Description is required", required=True)

productCategoryFields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String
}

# * Get Data
class GetData(Resource):
    @marshal_with(productCategoryFields)
    def get(self):
        productCategory = ProductCategoryModel.query.all()
        return productCategory
    
# * Detail Data
class DetailData(Resource):
    @marshal_with(productCategoryFields)
    def get(self, id):
        productCategory = ProductCategoryModel.query.get(id)
        if not productCategory:
            abort(404, message="ID Kategori Produk Tidak Ditemukan")
        return productCategory
            
# * Create Data
class CreateData(Resource):
    @marshal_with(productCategoryFields)
    def post(self):
        args = productCategory_args.parse_args()
        
        # Periksa apakah name sudah ada
        existing_name = ProductCategoryModel.query.filter_by(name=args['name']).first()
        if existing_name:
            abort(400, message="Nama Produk Kategori sudah digunakan")
        
        productCategory = ProductCategoryModel(name=args['name'], description=args['description'])
        db.session.add(productCategory)
        db.session.commit()
        return productCategory, 201

# * Update Data
class UpdateData(Resource):
    @marshal_with(productCategoryFields)
    def put(self, id):
        args = productCategory_args.parse_args()

        # Periksa ID
        productCategory = ProductCategoryModel.query.get(id)
        if not productCategory:
            abort(404, message="Product Category tidak ditemukan")
        
        # Periksa apakah username baru sudah digunakan oleh pengguna lain
        existing_name = ProductCategoryModel.query.filter(ProductCategoryModel.name == args['name'], ProductCategoryModel.id != id).first()
        if existing_name:
            abort(400, message="Nama Produk Kategori sudah digunakan")
        
        # Perbarui Data
        productCategory.name = args['name']
        productCategory.description = args['description']
        db.session.commit()
        return productCategory
    
    # * Delete Data
class DeleteData(Resource):
    def delete(self, id):
        productCategory = ProductCategoryModel.query.get(id)
        if not productCategory:
            return {"Message": "ID Product Category Tidak Ditemukan"}, 404
        try:
            db.session.delete(productCategory)
            db.session.commit()
            return {"Message": "Data Product Category Berhasil Dihapus"}, 200
        except:
            db.session.rollback()
            return {"Message": "Gagal Menghapus Data Product Category"}, 500