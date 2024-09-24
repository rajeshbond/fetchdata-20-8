
from datetime import datetime , date
from operator import le
from pydantic import BaseModel, EmailStr , conint
from typing import Optional
from app.models import *
from pydantic.types import conlist



# this is the old code start here 


#  The hash end here to be deleted later

class Nifty50(BaseModel):
    symbol : str
    lastPrice : float
    pChange : float
class Commodity(BaseModel):
    id: str
    lastprice: str
    percentchange: str
    lastupdate: str
    market_state: str

class Currency(BaseModel):
    name: str
    ltp: str
    chgper: str
    lastepoch: int
    market_state: str

class IndianARD(BaseModel):
    shortname: str
    lastprice: str
    percentchange: str
    upd_epoch: int
    market_state: str

class GlobalData(BaseModel):
    name: str
    price: str
    percent_change: str
    last_updated: int
    flag_url: str
    state: str
class indexinput(BaseModel):
    indexName: str

class allIndex(BaseModel):
    index : str
    last : float
    percentChange : float


    

    