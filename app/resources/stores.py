from flask import Flask, request
from flask_smorest import abort
import uuid
from flask_smorest import Blueprint
from flask.views import MethodView
from schemas import StoreInSchema, StoreUpdate
from models import StoreTable
from db import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


blp = Blueprint('stores',__name__,description='operations on stores')

@blp.route('/stores/<string:store_id>')
class Store(MethodView):

    @blp.response(200, StoreInSchema)
    def get(self, store_id):
        try:
            store = StoreTable.query.get_or_404(store_id)
            return store
        except SQLAlchemyError:
            abort(404, message = 'store not found')

    def delete(self, store_id):
        store = StoreTable.query.get_or_404(store_id)
        if not store:
            abort(404, message = f'Store with {store_id} not found')
        db.session.delete(store)
        db.session.commit()
        return {'message':'store deleted'}, 204
    
    @blp.arguments(StoreUpdate)
    @blp.response(200, StoreInSchema)
    def put(self, store_data, store_id):
        store = StoreTable.query.get(store_id)
        if store:
            store.name = store_data['name']
        else:
            abort(404, message = f'Store with {store_id} not found')
        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(404, message = 'error while updateing to database')
        return store

@blp.route('/stores')
class StoreList(MethodView):

    @blp.response(200, StoreInSchema(many=True))
    def get(self):
        stores = StoreTable.query.all()
        return stores
    

    @blp.arguments(StoreInSchema)
    @blp.response(200, StoreInSchema)
    def post(self,store_data):
        store = StoreTable(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(404, message = 'Store already exists')
        except SQLAlchemyError:
            abort(404, message = 'error while inserting to database')

        return store