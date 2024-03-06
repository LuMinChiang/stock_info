# -*- coding: utf-8 -*-

import mysql.connector
import twstock
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

def get_filter_3():
  db, db_cursor = connect_db(db_name="stock_info")
  query = "SELECT * FROM STOCK_INFO.filter_3 order by company_type;"
  db_cursor.execute(query)
  result = db_cursor.fetchall()
  current_datetime = datetime.datetime.now()

  # Extract the current year and month
  current_year = current_datetime.year
  current_month = current_datetime.month
  current_day = current_datetime.day
  file_name = "/result/filter_3/"+str(current_year)+"/"+str(current_month)+"/"+str(current_year)+"-"+str(current_month)+"-"+str(current_day)+"_filter_3.csv"
  filename = current_directory+file_name
  os.makedirs(os.path.dirname(filename), exist_ok=True)
  list_to_csv = []
  fields = ['股票編號','公司名稱']
  for row in result:
    company_num = row[1]
    print(company_num)
    temp = [company_num,twstock.codes[company_num].name]
    list_to_csv.append(temp)
  with open(filename, "w", encoding='utf-8') as f:
    write = csv.writer(f)
     
    write.writerow(fields)
    write.writerows(list_to_csv)
    # for row in result:
    #   company_num = row[0]
    #   # print(row)
    #   print(company_num,twstock.codes[company_num].name)
    #   f.write(str(company_num)+" " + twstock.codes[company_num].name + "\n")

  return filename

def insert_to_over_100MA(company_num,data_date, db, db_cursor, commit=False):
  # db, db_cursor = connect_db(db_name="STOCK_INFO")
  query = "select company_code from over_100MA where company_code=\""+company_num+"\" and data_date=\""+str(data_date)+"\""
  db_cursor.execute(query)
  # print(query)
  result = db_cursor.fetchall()
  if len(result)==0:
    query = "insert ignore into over_100MA (company_code,update_time,update_name,data_date) Values (\""+\
    company_num+"\",\""+str(datetime.datetime.now())+"\",\"py\",\""+str(data_date)+"\")"
    db_cursor.execute(query)
    if commit:
      db.commit()

def insert_to_monthly_avg_volume_over_2x(company_num,data_date,xtimes, db, db_cursor, commit=False):
  # db, db_cursor = connect_db(db_name="stock_info")
  query = "select company_code from monthly_avg_volume_over_2x where company_code=\""+company_num+"\" and data_date=\""+str(data_date)+"\""
  db_cursor.execute(query)
  # print(query)
  result = db_cursor.fetchall()
  if len(result)==0:
    query = "insert ignore into monthly_avg_volume_over_2x (company_code,update_time,update_name,data_date,x_times) Values (\""+\
    company_num+"\",\""+str(datetime.datetime.now())+"\",\"py\",\""+str(data_date)+"\",\""+str(xtimes)+"\")"
    db_cursor.execute(query)
    if commit:
      db.commit()

def insert_to_gain_over_3_5(company_num,data_date,gain_value, db, db_cursor, commit=False):
  # db, db_cursor = connect_db(db_name="stock_info")
  query = "select company_code from gain_over_3_5 where company_code=\""+company_num+"\" and data_date=\""+str(data_date)+"\""
  db_cursor.execute(query)
  # print(query)
  result = db_cursor.fetchall()

  if len(result)==0:
    query = "insert ignore into gain_over_3_5 (company_code,update_time,update_name,data_date,gain_value) Values (\""+\
    company_num+"\",\""+str(datetime.datetime.now())+"\",\"py\",\""+str(data_date)+"\",\""+str(gain_value)+"\")"
    db_cursor.execute(query)
    if commit:
      db.commit()

#取得距離給定日期(預設是今天)多久的資料，若day_num為1則取最新，100則是距今第100筆
def get_history_data_from_now(db, db_cursor, company_num="", day_num=1, non_zero=False, data_date=""):
  query = ""
  where_query = ""
  with open("get_history_data_from_now.sql","r") as f:
    query = f.read()
  if non_zero:
    where_query = "WHERE closing_price IS NOT NULL AND closing_price != 0 AND volume IS NOT NULL AND volume != 0"
    if data_date != "":
      where_query += ''' and data_date<="'''+data_date.strftime("%Y/%m/%d")+"\""
  else:
    if data_date != "":
      where_query = '''where data_date<="'''+data_date.strftime("%Y/%m/%d")+"\""
  # where_query += " LIMIT "+str(day_num+1)
  if company_num != "":
    if data_date != "":
      where_query += " AND company_code = '"+company_num+"' limit "+str(day_num+1)
    else:
      where_query += " WHERE company_code = '"+company_num+"' limit "+str(day_num+1)
  #   query = query.format(where_query,str(day_num))
  # else:
  #   query = query.format(where_query,str(day_num))
  query = query.format(where_query,str(day_num))
  # print(query)
  # db, db_cursor = connect_db(db_name="STOCK_INFO")
  db_cursor = db.cursor(dictionary=True)
  db_cursor.execute(query)
  # print(query)
  result = db_cursor.fetchall()
  return result

#取得給定日期(預設是今天)前一天的資料
def get_last_data(db, db_cursor, company_num="", non_zero=False, data_date=""):
  query = '''
            select 
              company_code,
              data_date,
              closing_price,
              volume
            FROM
              company_history_data
            {}
            order by data_date desc 
            limit 2
          '''
  if non_zero:
    where_query = "WHERE closing_price IS NOT NULL AND closing_price != 0 AND volume IS NOT NULL AND volume != 0"
    if data_date != "":
      where_query += ''' and data_date<="'''+data_date.strftime("%Y/%m/%d")+"\""
  else:
    if data_date != "":
      where_query = '''where data_date<="'''+data_date.strftime("%Y/%m/%d")+"\""
  # where_query += " LIMIT "+str(day_num+1)
  if company_num != "":
    if data_date != "" or non_zero:
      where_query += " AND company_code = '"+company_num+"'"
    else:
      where_query += " WHERE company_code = '"+company_num+"'"
  # where_query += " limit 2"
  query = query.format(where_query)
  # print(query)
  # db, db_cursor = connect_db(db_name="STOCK_INFO")
  db_cursor = db.cursor(dictionary=True)
  db_cursor.execute(query)
  # print(query)
  result = db_cursor.fetchall()
  if len(result)>1:
    return result[1]
  return 0


