import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def start_page():
    return FileResponse("templates/start.html")

@app.get("/login")
async def login_page():
    return FileResponse("templates/login.html")

@app.get("/register")
async def register_page():
    return FileResponse("templates/register.html")

@app.get("/exit")
async def exit_page():
    return {"message": "Tu możesz np. zamknąć sesję użytkownika"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
