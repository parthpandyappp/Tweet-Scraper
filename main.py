from flask import Flask, render_template, request
from flask_socketio import SocketIO
from twitter_scraper_fetcher import *
# from markov_bot import generate_bot_answer
import json
import config
import random

app = Flask(__name__)
socketio = SocketIO(app)

# Renders UI
@app.route("/")
def home():
  return render_template("homepage.html")

# Chat API - WebSocket
@socketio.on("send question")
def generate_message(body, methods=["POST"]):
  question = body["message"]
  twitter_handle = body["username"]
  
  tweets = get_user_tweets(twitter_handle)

  try:
    # Send the answer to the app, to display to the user
    # bot_answer = generate_bot_answer(twitter_handle, question)
    clean_tweets = clean_tweets_data(tweets)
    single_tweet = random.choice(clean_tweets)
    answer = {"username": twitter_handle, "message": single_tweet}
    socketio.emit("bot answer", answer, room=request.sid)
  except:
    bot_answer = "Sorry, I couldn't process that. Try again pleasea"
    error_message = {"username": twitter_handle, "message": bot_answer}
    socketio.emit("error", error_message, room=request.sid)

if __name__ == "__main__":
    socketio.run(app)

