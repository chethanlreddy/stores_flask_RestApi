from flask import Flask, request
from flask_smorest import abort
import uuid
from flask_smorest import Blueprint
from flask.views import MethodView
from schemas import ItemInSchema, ItemUpdate
from models import ItemTable
from db import db
from sqlalchemy.exc import SQLAlchemyError


blp = Blueprint('items',__name__,description='operations on items')

@blp.route('/items/<string:item_id>')
class Item(MethodView):

    @blp.response(200, ItemInSchema)
    def get(self, item_id):
        try:
            item = ItemTable.query.get_or_404(item_id)
            return item
        except SQLAlchemyError:
            abort(404, message = 'item not found')

    def delete(self, item_id):
        item = ItemTable.query.get_or_404(item_id)
        if not item:
            abort(404, message = f'item with {item_id} not found')
        db.session.delete(item)
        db.session.commit()
        return {'message': 'item deleted'}, 204

    @blp.arguments(ItemUpdate)
    @blp.response(200, ItemInSchema)
    def put(self, item_data, item_id):
        item = ItemTable.query.get(item_id)
        if item:
            item.price = item_data['price']
            item.name = item_data['name']
        else:
            abort(404, message = f'Item with {item_id} not found')
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(404, message = 'error while updateing to database')
        return item

@blp.route('/items')
class ItemList(MethodView):
    @blp.response(200, ItemInSchema(many=True))
    def get(self):
        items = ItemTable.query.all()
        return items

    @blp.arguments(ItemInSchema)
    @blp.response(200, ItemInSchema)
    def post(self, item_data):

        items = ItemTable.query.all()
        item_name = item_data['name']
        store_id = item_data['store_id']
        for i in items:
            if i.name == item_name and i.store.id == int(store_id):
                abort(404, message = f'item with {item_name} is present in store {store_id}')

        item = ItemTable(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError :
            abort(404, message = 'error while isnerting to database')

        return item
