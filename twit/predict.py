'''Prediction of User authorship based on Tweet Embeddings'''
import numpy as np
from sklearn.linear_model import LogisticRegression
from .db_model import User
from .twitter import nlp, vectorize_tweet


def predict_user(user1, user2, tweet_text):
    '''Determine and return which user is more likely to say a given tweet.
    # Arguments: 
        user1: str, twitter user name for user 1 in comparison from web form
        user2: str, twitter user name for user 2 in comparison from web form
        tweet_text: str, tweet text to evaluate from web form
    
    # Returns
       predction from logitstic regression model
    '''
    user1 = User.query.filter(User.username == user1).one()
    user2 = User.query.filter(User.username == user2).one()
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweet])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweet])

    # Combine embeddings and create labels
    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    labels = np.concatenate([np.ones(len(user1_embeddings)),
                             np.zeros(len(user2_embeddings))])

    # Train model and convert input text to embeddings
    log_reg = LogisticRegression(max_iter=1000).fit(embeddings, labels)
    tweet_embedding = vectorize_tweet(nlp, tweet_text)

    return log_reg.predict([tweet_embedding])[0]
    