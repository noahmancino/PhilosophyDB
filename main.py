import fastapi
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse("static/home/home.html")


@app.get("/hello/{name}")
async def say_hello(name: str):
    return FileResponse(f"static/hello/{name}.html")

@app.get("/contact")
async def contact():
    return FileResponse(f"static/contact/contact.html")