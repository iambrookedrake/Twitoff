from flask import Flask, render_template, request
from .db_model import DB, User
from .twitter import add_user_tweepy

def create_app():
    '''Create and configure an instance of our Flask application'''
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\iambr\\Desktop\\Unit3\\Twitoff\\twitoff.sqlite3'  # for absolute path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ENV'] = 'development' # Turns debug mode ON
    DB.init_app(app)  # Connect Flask app to SQLAlchemy DB

    @app.route('/')
    def root():
        return render_template('base.html', title='Home', users=User.query.all())

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def add_or_update_user(name=None, message=''):
        name = name or request.values['user_name']

        try:
            if request.method == "POST":
                add_user_tweepy(name)
                message = "User {} successfully added!".format(name)
            tweets = User.query.filter(User.username == name).one().tweet
        except Exception as e:
            print(f'Error adding {name}: {e}')
            tweets = []
            
        return render_template('user.html', title=name, tweets=tweets, message=message)

    return app