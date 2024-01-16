from fastapi import FastAPI, Body

app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "Hello from deep purple webscraper and AI"}
