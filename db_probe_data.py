import sys,os
import sqlalchemy
import mysql.connector
from sqlalchemy import BigInteger, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class db_probe_data(Base):

    __tablename__ = "probe_data"

    probeid = Column(Integer)
    probe_uid = Column(BigInteger, primary_key=True)
    datax = Column(Float)
    datay = Column(Float)
    dataz = Column(Float)
    temperature = Column(Float)
    RH = Column(Float)
    errory = Column(Float)
    time = Column(DateTime)
    bias_current = Column(Float)

    # def __repr__(self):
    #     return ("probe_data(uid='%s', pid='%s', x='%s', y='%s', z='%s', " +
    #            "temp='%s', humid='%s', err='%s', time='%s', bias_current='%s')"
    #            %(self.probeid,self.probe_uid,self.datax,self.datay,self.dataz,self.temperature,self.RH,self.errory,self.time,self.bias_current))
