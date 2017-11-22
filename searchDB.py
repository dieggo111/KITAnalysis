import sys,os
import sqlalchemy
import mysql.connector
from db_probe_data import db_probe_data
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import select
from sqlalchemy import or_

class searchDB(object):

    def __init__(self):

        db = {"host": "192.168.13.2",
              "port": "3306",
              "database": "sample",
              "user": "abfrage",
              "passwd": "JtjTN9M4WpQr,29t"}

        self.engine = sqlalchemy.create_engine("mysql+mysqlconnector://" +
                                          db["user"] + ":" + db["passwd"] +
                                          "@" + db["host"] + ":" + db["port"] + "/" + db["database"])

    def search(self,ID=None,Name=None):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        # session = Session.configure(bind=self.engine)
        data = session.query(db_probe_data).filter_by(probeid=ID)
        return data
        # conn = self.engine.connect()
        # meta = MetaData(self.engine,reflect=True)
        # table = meta.tables["probe_data"]
        # select_st = select([table]).where("probeid="+str(ID))
        # res = conn.execute(select_st)
        # for row in res:
        #     print(row)



if __name__ == '__main__':

    s = searchDB()
    for row in s.search(ID=39883):
        print(row.datax)
