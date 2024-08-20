
from enum import unique    # added 
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey , Float, BigInteger,Sequence, Date #added 
from sqlalchemy.sql.sqltypes import TIMESTAMP , Date , DateTime # added 
from sqlalchemy.orm import relationship # added 
from sqlalchemy.sql.expression import text  #added 
from .database import Base #added
# from msilib import sequence #added

from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Symbol(Base):
    __tablename__ = "Symbol"
    
    id = Column(Integer, primary_key=True, index=True)
    nsecode = Column(String)
    name_of_the_company = Column(String) 
    bsecode = Column(Integer, nullable=True) # Adjusted column name
    status = Column(String)  # Adjusted column name
    face_value = Column(Integer)  # Adjusted column name
    isin_number = Column(String)  # Adjusted column name
    igroup_name = Column(String)  # Adjusted column name
    create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class IntradayData(Base):
    __tablename__ = "IntradayData"
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

      # Adjusted column name
class OverBroughtData(Base):
    __tablename__ = "OverBroughtData"
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
  
class PositionalData(Base):
    __tablename__ = "PositionalData"
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

class ReversalData(Base):
    __tablename__ = "ReversalData"
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

class SwingData(Base):
    __tablename__ = "SwingData"
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

class Condition6(Base):
    __tablename__ = "Condition6"
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

# class DaySymbol(Base):
#     __tablename__ = "DaySymbol"
#     id = id = Column(BigInteger, primary_key=True, index=True)
#     nsecode = Column(String,nullable=False)
#     create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# class DayNSEData(Base):
#     __tablename__ = "DayNSEData"
#     id = id = Column(BigInteger, primary_key=True, index=True)
#     nsecode = Column(String, nullable=False)
#     ltp = Column(Float, nullable=False)
#     pChange = Column(Float, nullable=False)
#     create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



# class DayIndraday(Base):
#     __tablename__ = "DayIndraday"
#     id = Column(Integer, Sequence('DayIndraday_id_seq'), primary_key=True)
#     nsecode = Column(String, nullable=False)
#     per_chg = Column(Float, nullable=False)
#     close = Column(Float, nullable=False)
#     date = Column(String, nullable=False)
#     sector = Column(String, nullable=False)
#     count = Column(Integer, nullable=False)
#     frequency = Column(Integer, nullable=False)
#     create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# class DayOverBrought(Base):
#     __tablename__ = "DayOverBrought"
#     id = Column(Integer, Sequence('DayOverBrought_id_seq'), primary_key=True)
#     nsecode = Column(String, nullable=False)
#     per_chg = Column(Float, nullable=False)
#     close = Column(Float, nullable=False)
#     date = Column(String, nullable=False)
#     sector = Column(String, nullable=False)
#     count = Column(Integer, nullable=False)
#     frequency = Column(Integer, nullable=False)
#     create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# class DayPostional(Base):
#     __tablename__ = "DayPostional"
#     id = Column(Integer, Sequence('DayPostional_id_seq'), primary_key=True)
#     nsecode = Column(String, nullable=False)
#     per_chg = Column(Float, nullable=False)
#     close = Column(Float, nullable=False)
#     date = Column(String, nullable=False)
#     sector = Column(String, nullable=False)
#     count = Column(Integer, nullable=False)
#     frequency = Column(Integer, nullable=False)
#     create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# class DayReversal(Base):
#     __tablename__ = "DayReversal"
#     id = Column(Integer, Sequence('DayReversal_id_seq'), primary_key=True)
#     nsecode = Column(String, nullable=False)
#     per_chg = Column(Float, nullable=False)
#     close = Column(Float, nullable=False)
#     date = Column(String, nullable=False)
#     sector = Column(String, nullable=False)
#     count = Column(Integer, nullable=False)
#     frequency = Column(Integer, nullable=False)
#     create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# class DaySwing(Base):
#     __tablename__ = "DaySwing"
#     id = Column(Integer, Sequence('DaySwing_id_seq'), primary_key=True)
#     nsecode = Column(String, nullable=False)
#     per_chg = Column(Float, nullable=False)
#     close = Column(Float, nullable=False)
#     date = Column(String, nullable=False)
#     sector = Column(String, nullable=False)
#     count = Column(Integer, nullable=False)
#     frequency = Column(Integer, nullable=False)
#     create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))




