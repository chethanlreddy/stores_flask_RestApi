from flask import Flask
from flask_smorest import Api
from resources.items import blp as ItemBluePrint
from resources.stores import blp as StoreBluePrint
import models
import os
from db import db




def create_app(db_url = None):
    app = Flask(__name__)

    @app.get('/')
    def root_node():
        return {'message':'hello world'}



    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{config.setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}'
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DataBaseUrl","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False

    db.init_app(app)

    api = Api(app)

    @app.before_request
    def create_table():
        db.create_all()

    api.register_blueprint(ItemBluePrint)
    api.register_blueprint(StoreBluePrint)


    return app



# @app.get('/stores')
# def get_stores():
#     return {"stores": list(stores.values())}

# @app.post('/add-new-store')
# def add_new_store():
#     store_data = request.get_json()
#     store_id = uuid.uuid4().hex
#     store = {**store_data,"id":store_id}
#     stores[store_id] = store
#     return store, 201

# @app.get('/items')
# def get_items():
#     return {'items': list(items.values())}

# @app.post('/add-new-item')
# def add_new_item():
#     item_data = request.get_json()
#     if item_data['store_id'] not in stores:
#         abort(404, message = 'store not found')
#     item_id = uuid.uuid4().hex
#     item  = {**item_data,'id':item_id}
#     items[item_id] = item
#     return item, 201

# @app.get('/stores/<string:store_id>')
# def get_store(store_id):
#     try:
#         return stores[store_id]
#     except KeyError:
#         abort(404, message = 'store not found')
    
# @app.get('/item/<string:item_id>')
# def get_item(item_id):
#     try:
#         return items[item_id]
#     except KeyError:
#         abort(404, message = 'item not found')

# @app.delete('/store/delete-store/<string:store_id>')
# def remove_store(store_id):
#     if store_id not in stores.keys():
#         return {'message':'not found'}, 404
#     del stores[store_id]
#     return {'message':'sucess'}, 200

# @app.put('/store/update/<string:store_id>')
# def update_store(store_id):
#     store_data = request.get_json()
#     if store_id not in stores.keys():
#         return {'message':'store not found'}, 404
#     store = stores[store_id]
#     store |= store_data
#     return store, 201

# @app.delete('/item/delete-item/<string:item_id>')
# def remove_item(item_id):
#     if item_id not in items.keys():
#         abort(404, message='item not found')
#         # return {'message': 'item not found'}, 404
#     del items[item_id]
#     return {'message':'sucess'}, 200

# @app.put('/item/update/<string:item_id>')
# def update_item(item_id):
#     item_data = request.get_json()
#     if item_id not in items.keys():
#         return {'message':'item not found'}, 404
#     item = items[item_id]
#     item |= item_data
#     return item, 201