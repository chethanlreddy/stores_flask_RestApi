from flask import Flask, request
from flask_smorest import abort
import uuid
from flask_smorest import Blueprint
from flask.views import MethodView
from schemas import TagInSchema
from models import StoreTable, TagTable
from db import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

blp = Blueprint('tags',__name__,description='operations on tags')

@blp.route('/store/<string:tag_id>/tag')
class TagsInStore(MethodView):
    @blp.response(200, TagInSchema(many=True))
    def get(self, store_id):
        store_tag = StoreTable.query.get_or_404(store_id)
        if not store_tag:
            abort(404, message = f'No record found with {store_id}')
        return store_tag
    
    @blp.arguments(TagInSchema)
    @blp.response(201, TagInSchema)
    def post(self, tag_data, store_id):
        # if TagTable.query.filter(TagTable.store_id == store_id, TagTable.name == tag_data['name']).first():
        #     abort(404, message = 'tag with name already exist')
        tag = TagTable(**tag_data, store_id = store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(404, message  = f'error while inserting \n {e}')
        except IntegrityError as e:
            abort(404, message = f'intigity error \n {e}')
        return tag

@blp.route('/tag/<string:tag_id>')
class Tag(MethodView):
    @blp.response(200, TagInSchema)
    def get(tag_id):
        tag = TagTable.query.get_or_404(tag_id)
        return tag