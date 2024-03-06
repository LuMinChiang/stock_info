from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from DB import *
import os
import time
from time import sleep
import twstock
import datetime
from lxml import etree
from datetime import datetime, timedelta
import re
import sys
import requests
from twstock.proxy import get_proxies
import pandas as pd
from io import StringIO
import re
from get_data_lib import *
from email_lib import *

#計算歷史資料(5日線,10日線)
def calculate_5MA_10MA():
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	all_num = get_all_company_num(db,db_cursor)
	# calculate_history_data("1101", db, db_cursor)
	for company_num in all_num:
		print(company_num)
		calculate_5MA_10MA_history_data(company_num, db, db_cursor)
		db.commit()

#計算公司資料(5日線,10日線)
def calculate_5MA_10MA_history_data(company_num, db, db_cursor):
	query = "select * from company_history_data where company_code=\"%s\""
	with open("get_recent_260_data.sql","r") as f:
		query = f.read()
	# db, db_cursor = connect_db(db_name="STOCK_INFO")
	db_cursor.execute(query.format(company_num))
	result = db_cursor.fetchall()
	if len(result) < 20:
		print("not much data to calculate")
		return
	i = 0
	_5MA_flag = 0
	_5MA_sum = 0
	_10MA_flag = 0
	_10MA_sum = 0
	while i in range(len(result)):
		insert_5MA = None
		insert_10MA = None
		if result[i][2] != 0  and result[i][2] is not None:
			_5MA_sum += result[i][2]
		if result[i][2] != 0  and result[i][2] is not None:
			_10MA_sum += result[i][2]
		if result[i] is None:
			break
		if i>=5:
			_5MA_flag=1
		if i>=10:
			_10MA_flag=1

		if _5MA_flag:
			if result[i-5][2] != 0  and result[i-5][2] is not None:
				_5MA_sum -= result[i-5][2]
			insert_5MA = _5MA_sum/5
		if _10MA_flag:
			if result[i-10][2] != 0  and result[i-10][2] is not None:
				_10MA_sum -= result[i-10][2]
			insert_10MA = _10MA_sum/10

		print(result[i])
		print(i,insert_10MA,insert_5MA)
		if (insert_5MA is not None) or (insert_10MA is not None):
			if insert_5MA is None:
				insert_5MA = "NULL"
			if insert_10MA is None:
				insert_10MA = "NULL"
			query = '''
						update
							company_history_calculate_data
						set
							update_time="'''+str(datetime.now())+'''",
							10MA='''+str(insert_10MA)+''',
							5MA='''+str(insert_5MA)+''' 
						where data_date="'''+str(result[i][1]) + '''" and company_code="'''+company_num+'''"'''
			
			print(query)
			db_cursor.execute(query)
			# db.commit()
		# print(row)
		i+=1

	return

#補齊漲跌幅
def complete_calculate_gain_percentage(day_num=10):
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	all_num = get_all_company_num(db,db_cursor)
	for company_num in all_num:
		calculate_gain_percentage(company_num, db, db_cursor, day_num)
		db.commit()

def calculate_gain_percentage(company_num, db, db_cursor, day_num):
	query = "select * from company_history_data where company_code=\"%s\""
	with open("get_recent_260_data.sql","r") as f:
		query = f.read()
	# db, db_cursor = connect_db(db_name="STOCK_INFO")
	db_cursor.execute(query.format(day_num, company_num))
	result = db_cursor.fetchall()
	# if len(result) < 20:
	# 	print("not much data to calculate")
	# 	return
	i = 0
	last_closing_price = -1
	while i in range(len(result)):
		if result[i] is None:
			break
		print(result[i])
		current_closing_price = result[i][2]
		if current_closing_price is None:
			current_closing_price = 0

		if result[i][2] != 0  and result[i][2] is not None:
			# last_data = get_last_data(db, db_cursor, company_num, non_zero=True, data_date=result[i][1])
			# if last_data!=0:
			if last_closing_price > 0:
				# gain_percentage = (current_closing_price-last_data["closing_price"])/last_data["closing_price"]
				gain_percentage = (current_closing_price- last_closing_price)/last_closing_price
				if check_gain_percentage(company_num, db, db_cursor, result[i][1])==False:
					print(gain_percentage)
					query = '''
								update
									company_history_calculate_data
								set
									update_time="'''+str(datetime.now())+'''",
									gain_percentage='''+str(gain_percentage)+'''
								where data_date="'''+str(result[i][1]) + '''" and company_code="'''+company_num+'''"'''
					db_cursor.execute(query)
			last_closing_price = result[i][2]
		i+=1

def check_gain_percentage(company_num, db, db_cursor, data_date):
	query = '''
				select company_code from company_history_calculate_data 
				where data_date="'''+str(data_date) + '''" and company_code="'''+company_num+'''" and gain_percentage IS NOT NULL'''
	db_cursor = db.cursor(dictionary=True)
	db_cursor.execute(query)
	# print(query)
	result = db_cursor.fetchall()
	if len(result)>0:
		return True
	return False


