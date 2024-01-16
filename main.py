from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/favicon.ico")
async def favicon():
    print("fav")
    return FileResponse("static/favicon.ico")


@app.get("/")
async def hello():
    return {"message": "Hello from deep purple webscraper and AI"}
