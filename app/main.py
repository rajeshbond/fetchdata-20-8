 
from fastapi import FastAPI, Request, Response
from . import models
from .database import engine
from .routers import symbols, stock_price,screener,fetchdata,live
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles



models.Base.metadata.create_all(bind=engine) # commented becase now alembic is genetatic the table for us

app = FastAPI()

##### lIST OF origins

origins = ['*']


# #  pasting CORAS CODE #################
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# # #####################################
app.include_router(symbols.router)
app.include_router(stock_price.router)
app.include_router(screener.router)
app.include_router(fetchdata.router)
app.include_router(live.router)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
def add_cache_control_headers(response: Response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.get("/",response_class=HTMLResponse)
def root(request: Request):
    response = templates.TemplateResponse("index.html",{"request": request})
    # response = templates.TemplateResponse("notfound.html",{"request": request})
    response = add_cache_control_headers(response)
    return response

