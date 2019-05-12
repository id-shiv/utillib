from flask import Flask
from textblob import TextBlob

app = Flask(__name__)

@app.route('/<msg>')
def index(msg):
    sentiment = 'postive'
    if TextBlob(msg).sentiment.polarity < 0.0:
        sentiment = 'negative'

    return app.make_response(sentiment)