from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()


class User(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)
    username = DB.Column(DB.String(80), unique=True, nullable=False)
    followers = DB.Column(DB.String(120), unique=True, nullable=False)
    # Tweets IDs are ordinal ints, so we can fetch most recent data
    newest_tweet_id = DB.Column(DB.BigInteger, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Tweet(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)
    tweet = DB.Column(DB.String(300), unique=True, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweet', lazy=True))
    embedding = DB.Column(DB.PickleType, nullable=False)

    def __repr__(self):
        return '<Tweet %r>' % self.tweet


# To create the database:
# from twit.db_model import DB, User, Tweet
# DB.create_all()
# to reset
# DB.drop_all()
