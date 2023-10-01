from db import db

class StoreTable(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    item = db.relationship('ItemTable', back_populates='store', lazy = 'dynamic', cascade = 'all, delete')
    tags = db.relationship('TagTable', back_populates='store', lazy = 'dynamic', cascade = 'all, delete')