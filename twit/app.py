from flask import Flask
from .db_model import DB, User


def create_app():
    '''Create and configure an instance of our Flask application'''
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\iambr\\Desktop\\Unit3\\Twitoff\\twitoff1.sqlite3'  # for absolute path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)  # Connect Flask app to SQLAlchemy DB

    @app.route('/')
    def root():
        return 'Welcome to Twitoff!'

    @app.route('/<username>/<followers>')
    def add_user(username, followers):
        user = User(username=username, followers=followers)
        DB.session.add(user)
        DB.session.commit()

        return f'{username} has been added to the DB!'

    return app
