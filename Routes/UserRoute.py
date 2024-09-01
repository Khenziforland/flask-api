from flask_restful import Api
from Controllers.UserController import GetData, DetailData, CreateData, UpdateData, DeleteData

userApi = Api()

# * User Routes
userApi.prefix = '/api/users'

userApi.add_resource(GetData, "/", endpoint="get_users", methods=["GET"])
userApi.add_resource(DetailData, "/<string:id>", endpoint="get_user_detail", methods=["GET"])
userApi.add_resource(CreateData, "/", endpoint="create_user", methods=["POST"])
userApi.add_resource(UpdateData, "/<string:id>", endpoint="update_user", methods=["PUT"])
userApi.add_resource(DeleteData, "/<string:id>", endpoint="delete_user", methods=["DELETE"])