from textblob import TextBlob

def get_sentiment(text):
    return TextBlob(text).sentiment.polarity