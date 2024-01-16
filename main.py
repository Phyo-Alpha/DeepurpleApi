from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from typing import List
from pydantic import BaseModel

from transformers import pipeline
from tweety import Twitter


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

classifier = pipeline(
    task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None
)

classifier_2 = pipeline(
    task="text-classification", model="distilbert-base-uncased-finetuned-sst-2-english"
)


class Sentences(BaseModel):
    sentences: List[str]


@app.get("/favicon.ico")
async def favicon():
    print("fav")
    return FileResponse("static/favicon.ico")


@app.get("/")
async def hello():
    return {"message": "Hello from deep purple webscraper and AI"}


@app.post("/predict")
async def predict(sentences: Sentences):
    model_outputs = classifier(sentences.sentences)

    for i, output in enumerate(model_outputs):
        print(f"Text : {sentences.sentences[i]}")
        for emotion in output:
            if emotion["score"] < 0:
                pass
            else:
                print(f"{emotion['label']} : {emotion['score']}")
        print("\n")


@app.get("/tweets/{username}")
async def get_tweets(username: str):
    user_tweets = {}

    app = Twitter("session")
    app.sign_in("edwardphyoo", "35571559")
    target_username = username

    user_info = app.get_user_info(target_username)
    all_tweets = app.get_tweets(target_username, pages=1)

    user_tweets["name"] = user_info.name
    user_tweets["username"] = user_info.username
    user_tweets["tweets"] = []
    for tweet in all_tweets:
        try:
            user_tweet = {
                "tweet-id": tweet.id,
                "tweet": tweet.text,
                "date": tweet.created_on,
                "likes": tweet.likes,
                "views": tweet.views,
                "reply_count": tweet.reply_counts,
                "replies": [],
            }
            stop = False
            for thread in tweet.get_comments(pages=1, wait_time=2):
                if stop:
                    break
                for reply in thread.tweets:
                    user_comment = {
                        "author": reply.author.username,
                        "comment": reply.text,
                    }
                    user_tweet.get("replies").append(user_comment)

                    if len(user_tweet.get("replies")) >= 2:
                        stop = True
                        break
            user_tweets.get("tweets").append(user_tweet)
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

    return user_tweets
