from flask import Flask
from db import db
from flask_restful import Api
from Routes.UserRoute import userApi
from Routes.ProductCategory import productCategoryApi

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db.init_app(app)

# * User Routes
userApi.init_app(app)

# * Product Category Routes
productCategoryApi.init_app(app)

@app.route('/')
def home():
    return '<h1>Hello World</h1>'

if __name__ == '__main__':
    app.run(debug=True)