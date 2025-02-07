from sqlalchemy import MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from app import db




metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    reviews = relationship('Review', back_populates='customer', cascade='all, delete-orphan')

    items = association_proxy('reviews', 'item')

    serialize_rules = ('-reviews.customer',) 



class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'
 
    reviews = relationship('Review', back_populates='item', cascade='all, delete-orphan')

    serialize_rules = ('-reviews.item',) 

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    customer = relationship('Customer', back_populates='reviews')
    item = relationship('Item', back_populates='reviews')

    serialize_rules = ('-customer.reviews', '-item.reviews')