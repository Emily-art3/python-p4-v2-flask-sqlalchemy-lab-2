from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata) 

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db) 

    with app.app_context():  
        from models import Customer, Item, Review
        db.create_all()

    @app.route('/')
    def index():
        return '<h1>Flask SQLAlchemy Lab 2</h1>'

    return app

app = create_app() 

if __name__ == '__main__':
    app.run(port=5555, debug=True)
