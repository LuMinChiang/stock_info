import mysql.connector
import datetime
import os
import csv

current_directory = os.getcwd()

def connect_db(db_name, host_ip="127.0.0.1",user_name="root",pw="bruce0912"):
  db = mysql.connector.connect(
    host = host_ip,
    user = user_name,
    password = pw,
    database = db_name,
    )
  cursor=db.cursor()
  return db, cursor