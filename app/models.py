
from enum import unique    # added 
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey , Float, BigInteger,Sequence, Date #added 
from sqlalchemy.sql.sqltypes import TIMESTAMP , Date , DateTime # added 
from sqlalchemy.orm import relationship # added 
from sqlalchemy.sql.expression import text  #added 
from .database import Base #added
# from msilib import sequence #added

from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class TestData(Base):
    __tablename__ = "TestData"
    id = Column(BigInteger, primary_key=True, index=True)
    nsecode = Column(String,nullable=True)
    name = Column(String,nullable=False)
    bsecode = Column(Integer, nullable=True)
    per_chg = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(BigInteger, nullable = False)
    date = Column(String,nullable=False)
    time = Column(String,nullable=False)
    igroup_name = Column(String)
    create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class FIIDII(Base):
    __tablename__ = "FIIDII"
    id = Column(BigInteger, primary_key=True, index=True)
    DII = Column(String,nullable=False)
    DIIBuyValue = Column(Float,nullable=False)
    DIISellValue = Column(Float,nullable=False)
    DIINetValue = Column(Float,nullable=False)
    FII = Column(String,nullable=False)
    FIIbuyValue = Column(Float,nullable=False)
    FIIsellValue = Column(Float,nullable=False)
    FIInetValue = Column(Float,nullable=False)
    date = Column(String,nullable=False)
    time = Column(String,nullable=False)
    create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))