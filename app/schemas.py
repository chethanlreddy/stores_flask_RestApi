from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemInSchema(PlainItemSchema):
    store_id = fields.Str(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only = True)


class StoreInSchema(PlainStoreSchema):
    item = fields.List(fields.Nested(PlainItemSchema()), dump_only =True)


class StoreUpdate(Schema):
    name = fields.Str()
    id = fields.Str(dump_only=True)

class ItemUpdate(Schema):
    store_id = fields.Str(dump_only=True)
    id = fields.Str(dump_only=True)
    name = fields.Str()
    price = fields.Float()