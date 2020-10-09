from flask import Flask, render_template, request
from .db_model import DB, User, Tweet
from .twitter import add_user_tweepy, update_all_users
from .predict import predict_user
from dotenv import load_dotenv
from os import getenv
load_dotenv()

def create_app():
    '''Create and configure an instance of our Flask application'''
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
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

    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1 = request.values['user1']
        user2 = request.values['user2']
        tweet_text = request.values['tweet_text']

        if user1 == user2:
            message = 'Cannot compare a user to themselves! Select a second User.'
        else:
            prediction = int(predict_user(user1, user2, tweet_text)*100)
            if prediction >= 50:
                message = f'"{tweet_text}" is more likely to be said by {user1} than {user2}, with {prediction}% confidence.'
            else:
                message = f'"{tweet_text}" is more likely to be said by {user2} than {user1}, with {100-prediction}% confidence.'
        
        return render_template('predict.html', title='Prediction', message=message)

    @app.route('/reset304')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset!', users=User.query.all())


    @app.route('/update', methods=['GET'])
    def update():
        update_all_users()
        return render_template('base.html', title='All Tweets Updated!', users=User.query.all())

    return app