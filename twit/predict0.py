'''Prediction of Users based on Tweet embeddings'''
import numpy as np
from sklearn.linear_model import LogisticRegression
from .model import db, User, Tweet
from .twitter import BASILICA


def predict_user(user1, user2, tweet_text):
    '''Determine and return which user is more likely to say a given tweet.
    # Arguments:
        user1: str, twitter user name for user 1 in comparison from web form
        user2: str, twitter user name for user 1 in comparison from web form
        tweet_text: str, tweet text to evaluate
    # Returns:
        prediction from logistic regression model
    '''
    user1 = User.query.filter(User.username == user1).one()
    user2 = User.query.filter(User.username == user2).one()
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweet])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweet])
    
    # Combine embeddings and create labels
    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    labels = np.concatenate([np.ones(len(user1_embeddings)), 
                             np.zeros(len(user2_embeddings))])

    # Train model and convert input text to embedding
    log_reg = LogisticRegression(solver='lbfgs', max_iter=1000)
    log_reg.fit(embeddings, labels)
    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')
    return log_reg.predict_proba(np.array([tweet_embedding]))[:,1]
