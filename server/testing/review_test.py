import pytest
from app import app, db
from models import Customer, Item, Review

@pytest.fixture(scope='module')
def test_client():
    flask_app = app
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with flask_app.app_context():
        db.create_all()
        yield flask_app.test_client()
        db.session.remove()
        db.drop_all()

class TestReview:
    '''Review model in models.py'''

    def test_can_be_instantiated(self):
        '''can be invoked to create a Python object.'''
        r = Review(comment="Test Review") 
        assert r is not None
        assert isinstance(r, Review)

    def test_has_comment(self):
        '''can be instantiated with a comment attribute.'''
        r = Review(comment="great product!")  
        assert hasattr(r, "comment")
        assert r.comment == "great product!"

    def test_can_be_saved_to_database(self, test_client):
     with app.app_context():
        assert 'comment' in Review.__table__.columns

        customer = Customer(name="Test Customer")
        item = Item(name="Test Item", price=9.99)
        db.session.add_all([customer, item])
        db.session.commit()

        r = Review(comment="great!", customer=customer, item=item)
        db.session.add(r)
        db.session.commit()

        assert Review.query.count() == 1


    def test_is_related_to_customer_and_item(self, test_client):
     with app.app_context():
        db.session.query(Review).delete()
        db.session.commit()

        c = Customer(name="Test Customer")
        i = Item(name="Test Item", price=9.99)
        db.session.add_all([c, i])
        db.session.commit()

        r = Review(comment="great!", customer=c, item=i)
        db.session.add(r)
        db.session.commit()

        # Check foreign keys
        assert r.customer_id == c.id
        assert r.item_id == i.id
        # Check relationships
        assert r.customer == c
        assert r.item == i
        assert r in c.reviews
        assert r in i.reviews

        assert Review.query.count() == 1  

