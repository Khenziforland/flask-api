from flask_restful import Api
from Controllers.ProductCategoryController import GetData, DetailData, CreateData, UpdateData, DeleteData

productCategoryApi = Api()

# * Product Category Routes
productCategoryApi.prefix = '/api/product-categories'

productCategoryApi.add_resource(GetData, "/", endpoint="get_product_categories", methods=["GET"])
productCategoryApi.add_resource(DetailData, "/<string:id>", endpoint="get_product_category_detail", methods=["GET"])
productCategoryApi.add_resource(CreateData, "/", endpoint="create_product_category", methods=["POST"])
productCategoryApi.add_resource(UpdateData, "/<string:id>", endpoint="update_product_category", methods=["PUT"])
productCategoryApi.add_resource(DeleteData, "/<string:id>", endpoint="delete_product_category", methods=["DELETE"])