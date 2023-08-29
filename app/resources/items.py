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
        raise NotImplementedError('Deleting an element is not implemented')

    @blp.arguments(ItemUpdate)
    @blp.response(200, ItemInSchema)
    def put(self, item_data, item_id):
        item = ItemTable.query.get_or_404(item_id)
        raise NotImplementedError('updating an element is not implemented')
    

@blp.route('/items')
class ItemList(MethodView):
    @blp.response(200, ItemInSchema(many=True))
    def get(self):
        return list(items.values())

    @blp.arguments(ItemInSchema)
    @blp.response(200, ItemInSchema)
    def post(self, item_data):
        item = ItemTable(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(404, message = 'error while isnerting to database')
        return item, 201
