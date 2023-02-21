
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from starlette.responses import RedirectResponse
from .routers import user
from . import models
from .database import engine

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(user.router)



@app.get("/", tags=["authentication"])
def index():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)