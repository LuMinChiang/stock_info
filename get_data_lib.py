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
from selenium.webdriver.common.keys import Keys

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

current_directory = os.getcwd()
driver_directory = current_directory+"/chromedriver-mac-arm64/chromedriver"
if sys.platform.startswith('linux'): # 包含 linux 與 linux2 的情況
    current_directory = "/finance"
    driver_directory = current_directory+"/chromedriver-linux64/chromedriver"
    print("Linux",driver_directory)
elif sys.platform.startswith('darwin'):
	current_directory = os.getcwd()
	driver_directory = current_directory+"/chromedriver-mac-arm64/chromedriver"
	print("MacOS")
# current_directory = "/finance"
# driver_directory = current_directory+"/chromedriver-mac-arm64/chromedriver"
# driver_directory = current_directory+"/chromedriver-linux64/chromedriver"
#寫error log
def write_error_log(error,msg=""):
	current_datetime = datetime.now()

	# Extract the current year and month
	current_year = current_datetime.year
	current_month = current_datetime.month
	current_day = current_datetime.day
	print("error:"+msg)
	print(error.args)
	error_log_name = "/error_log/"+str(current_year)+"/"+str(current_month)+"/"+str(current_year)+"-"+str(current_month)+"-"+str(current_day)+"_error_log"
	filename = current_directory+error_log_name
	print(filename)
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	print(filename)
	with open(filename, "a") as f:
		f.write(str(msg)+"\n")
		f.write(str(error))
		# for msg in error.args:
		# 	f.write(str(msg))
		f.write("\n##########################\n")

#寫log
def write_log(msg):
	current_datetime = datetime.now()

	# Extract the current year and month
	current_year = current_datetime.year
	current_month = current_datetime.month
	current_day = current_datetime.day
	file_name = "/log/"+str(current_year)+"/"+str(current_month)+"/"+str(current_year)+"-"+str(current_month)+"-"+str(current_day)+"_log"
	filename = current_directory+file_name
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	# print(filename)
	with open(filename, "a") as f:
		f.write(str(msg)+"\n")

#main
#更新上市、上櫃資料
def update_company_list():
	print("check company update")
	try_time=0
	while try_time < 2:
		try:
			print(try_time)
			twstock.__update_codes()
			break
		except BaseException as e:
			print(str(e))
			try_time+=1
			continue
	#台灣證券交易所
	print("update_company")
	update_company();
	# listed_company_url = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
	# OTC_company_url = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=4"
	# write_log("update listed company")
	# update_company(listed_company_url,"1")
	# write_log("update OTC company url")
	# update_company(OTC_company_url,"2")

#not work due to limited frquency
#抓資本額
def get_capital_amount(company_num):
	# cService = webdriver.ChromeService(executable_path=driver_directory)
	# options = webdriver.ChromeOptions()
	# options.add_argument("--headless")
	# driver = webdriver.Chrome(service=cService, options=options)
	driver = open_webdriver()
	url = "https://goodinfo.tw/tw/StockDetail.asp?STOCK_ID="+str(company_num)
	driver.get(url)
	driver.implicitly_wait(15)
	content = driver.page_source

	box = driver.find_element(By.XPATH,"/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/table[1]/tbody/tr[5]/td[2]/nobr")
	print(box.text)
	capital_amount = box.text
	driver.quit()
	sleep(3)
	return capital_amount

#更新公司資料(使用套件)
def update_company():
	all_company = []
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	# cService = webdriver.ChromeService(executable_path=driver_directory)
	# options = webdriver.ChromeOptions()
	# options.add_argument("--headless")
	# options.add_argument("--no-sandbox")
	# options.binary_location = "/opt/google/chrome/chrome"
	# driver = webdriver.Chrome(service=cService, options=options)
	# url = "https://mops.twse.com.tw/mops/web/t05st03"
	# driver.get(url)
	# driver.implicitly_wait(15)
	for code in twstock.codes:
	# print(code)
		if twstock.codes[code].type == "股票":
			stock_data = []
			print(code)
			# print(twstock.codes[code])
			# update_company_data(twstock.codes[code].code, twstock.codes[code].name, twstock.codes[code].market,get_capital_amount(twstock.codes[code].code))
			update_company_data(twstock.codes[code].code, twstock.codes[code].name, twstock.codes[code].market, db, db_cursor)
			
			# all_company.append.append(stock_data)
	check_company_alive(db, db_cursor)
	# driver.quit()

#檢查公司是否下市
def check_company_alive(db, db_cursor):
	# db, db_cursor = connect_db(db_name="STOCK_INFO")
	query = "select company_code from company_id;"
	db_cursor.execute(query)
	result = db_cursor.fetchall()
	for row in result:
		company_num = row[0]
		print(company_num)
		if str(company_num).strip() in twstock.codes:
			print("alive")
			query = "update company_id set alive=\"alive\" where company_code=\""+company_num+"\";"
		else:
			print("dead")
			query = "update company_id set alive=\"dead\"where company_code=\""+company_num+"\";"
		db_cursor.execute(query)
		db.commit()

def check_company_insert(company_num, company_name, company_type, db, db_cursor):
	# db, db_cursor = connect_db(db_name="STOCK_INFO")
	db_cursor = db.cursor(dictionary=True)
	query = "select company_name, company_type from company_id where company_code=\""+str(company_num)+"\";"
	db_cursor.execute(query)
	result = db_cursor.fetchall()
	if len(result)<=0:
		return "insert"
	org_company_data = result[0]
	# org_capital_amount = ""
	# if org_company_data["capital_amount"] is not None:
	# 	org_capital_amount = str(org_company_data["capital_amount"]).strip()
	if company_name!=str(org_company_data["company_name"]).strip() or company_type!=str(org_company_data["company_type"]).strip():
		return "update"
	return

#儲存公司資料
def update_company_data(company_num, company_name, company_type, db, db_cursor):
	# db, db_cursor = connect_db(db_name="STOCK_INFO")
	now = time.strftime('%Y-%m-%d %H:%M:%S')
	# if capital_amount == "":
	# 	capital_amount = get_capital_amount_tw(company_num,driver)
	insert_flag = check_company_insert(company_num,company_name,company_type, db, db_cursor)
	if insert_flag == "insert":
		print("insert")
		# capital_amount = get_capital_amount_tw(company_num,driver)
		# query = "insert ignore into"+" company_id (company_code,company_name,company_type,update_time,capital_amount,update_name) VALUES (\""+\
		# 	company_num+"\",\""+company_name+"\",\""+company_type+"\",\""+now+"\",\""+capital_amount+"\",\"py\");"
		query = "insert ignore into"+" company_id (company_code,company_name,company_type,update_time,update_name) VALUES (\""+\
			company_num+"\",\""+company_name+"\",\""+company_type+"\",\""+now+"\",\"py\");"
		print(query)
		db_cursor.execute(query)
		db.commit()
	elif insert_flag == "update":
		print("update")
		# query = "update company_id set company_code=\""+company_num+"\", company_name=\""+company_name+\
		# 		"\", company_type=\""+company_type+"\","+"update_time=\""+now+"\", update_name=\"py\","+\
		# 		" capital_amount=\""+capital_amount+"\" where company_code=\""+company_num+"\""
		query = "update company_id set company_code=\""+company_num+"\", company_name=\""+company_name+\
				"\", company_type=\""+company_type+"\","+"update_time=\""+now+"\", update_name=\"py\""+\
				" where company_code=\""+company_num+"\""
		# print(query)
		# val = (company_num.replace("'",""),company_name.replace("'",""),company_type.replace("'",""),now.replace("'",""),capital_amount.replace("'",""),company_num.replace("'",""))
		
		# print((query,val))
		# db_cursor.execute(query,val)
		db_cursor.execute(query)
		db.commit()
	else:
		print("continue")
		return

#更新公司資料(爬網站)
def update_company_2(url,company_type):
	# cService = webdriver.ChromeService(executable_path=driver_directory)
	# options = webdriver.ChromeOptions()
	# options.add_argument("--headless")
	# driver = webdriver.Chrome(service=cService, options=options)

	# driver.get(url)
	driver = open_webdriver(url)
	driver.implicitly_wait(15)
	content = driver.page_source
	#print(type(content))
	#print(content)


	now = time.strftime('%Y-%m-%d %H:%M:%S')
	# with open(current_directory+"/website_content.html", "w") as f:
	#     f.write(content)

	#table = driver.find_element_by_class_name("h4")
	table = driver.find_element(By.CLASS_NAME, "h4")
	# rows = table.find_elements_by_tag_name("tr")
	rows = table.find_elements(By.TAG_NAME, "tr")
	#print(rows)
	data = []
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	i = 0
	start = 0
	for row in rows:
		# print(start)
		
		company_data = row.find_element(By.TAG_NAME, "td").text.split()
		if len(company_data) <=1:
			print(company_data[0])
			if company_data[0].find("股票")==-1:
				start = 0
			else :
				start = 1
			continue
		
		if start == 0:
			continue

		# if i > 1:
		# 	break;
		# i += 1
		company_num = company_data[0]
		company_name = company_data[1]
		capital_amount = get_capital_amount(company_num)
		print(company_num)

		query = "insert ignore into"+" company_id (company_code,company_name,company_type,update_time,capital_amount,update_name) VALUES (\""+\
				company_num+"\",\""+company_name+"\","+company_type+",\""+now+"\",\""+capital_amount+"\",\"py\");"
		print(query)
		db_cursor.execute(query)
		db.commit()

		query = "update company_id set company_code=\""+company_num+"\", company_name=\""+company_name+\
				"\", company_type="+company_type+","+"update_time=\""+now+"\", update_name=\"py\","+\
				" capital_amount=\""+capital_amount+"\" where company_code=\""+company_num+"\""
		print(query)
		# val = (company_num.replace("'",""),company_name.replace("'",""),company_type.replace("'",""),now.replace("'",""),capital_amount.replace("'",""),company_num.replace("'",""))
		
		# print((query,val))
		# db_cursor.execute(query,val)
		db_cursor.execute(query)
		db.commit()
		# print(company_num + "+" + company_name)

		# company_data = row.find_element(By.TAG_NAME, "td").text
		# data.append(company_data)
	db_cursor.close()
	db.close()
	driver.quit()
	# return data

#取得該公司的歷史資料，最早從2010/1開始
def get_company_history_data(company_num):
	# if company_num in twstock.codes
	info = twstock.codes[company_num]
	start_time = info.start.split("/")
	

	stock = twstock.Stock(company_num)
	datas=[]
	if int(start_time[0]) > 2010:
		print(start_time[0] + " " + start_time[1])
		datas = stock.fetch_from(int(start_time[0]),int(start_time[1]))
	else:
		print("2023 01")
		datas = stock.fetch_from(2023,1)
		# datas = stock.fetch_from(2024,1)
	# datas = stock.fetch_from(2010,1)
	# datas = stock.fetch_from(2023,12)
	insert_data = []
	i=0
	date_format = "%Y/%m/%d"
	for d in datas:
		i+=1
		time = d.date.strftime("%Y/%m/%d")
		detail = (datetime.strptime(time,date_format),d.close,d.capacity,d.open,d.high,d.low)
		# print(detail)
		insert_data.append(detail)
		# if i >= 50:
		# 	break
	# print(insert_data)
	return insert_data	

def check_history_company_insert(company_num, data_date, db, db_cursor):
	# db, db_cursor = connect_db(db_name="STOCK_INFO")
	# db_cursor = db.cursor(dictionary=True)
	query = "select open_price from company_history_data where company_code=\""+str(company_num)+"\" and data_date=\""+str(data_date)+"\";"
	print(query)
	db_cursor.execute(query)
	result = db_cursor.fetchall()
	print(result)
	if len(result)<=0:
		print("insert")
		return "insert"
	if result[0][0] is None:
		print("update")
		return "update"
	return


def sub_insert_data(company_num, insert_datas, db, db_cursor):
	query = ""
	now = time.strftime('%Y-%m-%d %H:%M:%S')
	for insert_data in insert_datas:
		print(insert_data)
		insert_flag = check_history_company_insert(company_num, insert_data[0], db, db_cursor)
		insert_data = trans_raw_data(insert_data)
		if insert_flag == "insert":
			query = "insert ignore into company_history_data (company_code,update_time,data_date,closing_price,volume,update_name,open_price,high_price,low_price) VALUES (\""+\
					str(company_num)+"\",\""+now+"\",\""+str(insert_data[0])+"\","+str(insert_data[1])+","+str(insert_data[2])+",\"py\","\
					+str(insert_data[3])+","+str(insert_data[4])+","+str(insert_data[5])+");"
			print(query)
		elif insert_flag == "update":
			query = "update company_history_data SET update_time=\""+now+"\",update_name=\"py\",open_price="+str(insert_data[3])+",high_price="+str(insert_data[4])+",low_price="+str(insert_data[5])+\
			" where data_date=\""+str(insert_data[0])+"\" and company_code=\""+company_num+"\";"
			print(query)
					
		db_cursor.execute(query)

def initial_all_company_history_data():
	# pre_url = "https://goodinfo.tw/tw/StockDetail.asp?STOCK_ID="	
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	query = "select company_code from company_id where alive=\"alive\";"
	db_cursor.execute(query)
	result = db_cursor.fetchall()
	# i = 0

	for row in result:
		# i+=1
		company_num = str(row[0]).strip()
		# if int(company_num) < 5607:
		# 	continue
		now = time.strftime('%Y-%m-%d %H:%M:%S')
		# url = "https://goodinfo.tw/tw/ShowK_Chart.asp?STOCK_ID=" + company_num + "&CHT_CAT2=DATE"
		print(row[0])
		# print(url)
		# save_company_data(company_num,url)
		# if 1:
		try:
			insert_datas = get_company_history_data(company_num)
			sub_insert_data(company_num, insert_datas, db, db_cursor)

			# if len(insert_datas)>1:
			# 	print(len(insert_datas))
			# # print(insert_data)
			# 	for insert_data_month in insert_datas:
			# 		sub_insert_data(company_num, insert_data_month, db, db_cursor)
			# else:
			# 	sub_insert_data(company_num, insert_datas, db, db_cursor)
			db.commit()
		except BaseException as error:
			write_error_log(error,company_num)
			continue
		# if i >= 1:
		# 	break

#儲存該公司的歷史資料
def add_company_history_data(company_num, db, db_cursor):
	# company_num = row[0]
	# if int(company_num) < 5607:
	# 	continue
	print(company_num)
	now = time.strftime('%Y-%m-%d %H:%M:%S')
	# db, db_cursor = connect_db(db_name="STOCK_INFO")
	# url = "https://goodinfo.tw/tw/ShowK_Chart.asp?STOCK_ID=" + company_num + "&CHT_CAT2=DATE"
	# print(row[0])
	# print(url)
	# save_company_data(company_num,url)
	# if 1:
	try:
		insert_datas = get_company_history_data(str(company_num))
		# print(insert_data)
		for insert_data in insert_datas:
			insert_data = trans_raw_data(insert_data)
			query = "insert ignore into company_history_data (company_code,update_time,data_date,closing_price,volume,update_name,open_price,high_price,low_price) VALUES (\""+\
						str(company_num)+"\",\""+now+"\",\""+str(insert_data[0])+"\","+str(insert_data[1])+","+str(insert_data[2])+",\"py\","\
						+str(insert_data[3])+","+str(insert_data[4])+","+str(insert_data[5])+");"
			query = "insert ignore into company_100_data (company_code,update_time,data_date,closing_price,volume,update_name,open_price,high_price,low_price) VALUES (\""+\
						str(company_num)+"\",\""+now+"\",\""+str(insert_data[0])+"\","+str(insert_data[1])+","+str(insert_data[2])+",\"py\","\
						+str(insert_data[3])+","+str(insert_data[4])+","+str(insert_data[5])+");"
			# print(query)
			db_cursor.execute(query)
			insert_calculate_history_data(company_num, insert_data, db, db_cursor)
		# db.commit()
	except BaseException as error:
		write_error_log(error,company_num)
		pass

#取得該公司的當月資料
def get_company_current_data(company_num,latest_data_date):
	company_num=str(company_num)
	stock = twstock.Stock(company_num)
	datas=[]
	# Get the current date and time
	current_datetime = datetime.now()

	# Extract the current year and month
	# current_year = current_datetime.year
	# current_month = current_datetime.month

	current_year = latest_data_date.year
	current_month = latest_data_date.month
	# datas = stock.fetch_from(2010,1)
	datas = stock.fetch_from(current_year,current_month)
	insert_data = []
	i=0
	date_format = "%Y/%m/%d"
	for d in datas:
		i+=1
		time = d.date.strftime("%Y/%m/%d")
		detail = (datetime.strptime(time,date_format),d.close,d.capacity,d.open,d.high,d.low)
		# print(type(time),time)
		# print(detail)
		insert_data.append(detail)
		# if i >= 50:
		# 	break
	# print(insert_data)
	return insert_data

# 處理None
def trans_raw_data(data):
	close_price = 0
	if data[1] is not None or data[1]=="None":
		close_price = data[1]
	open_price = 0
	if data[3] is not None or data[3]=="None":
		open_price = data[3]
	high_price = 0
	if data[4] is not None or data[4]=="None":
		high_price = data[4]
	low_price = 0
	if data[5] is not None or data[5]=="None":
		low_price = data[5]
	price_change = 0
	if data[6] is not None or data[6]=="None":
		price_change = data[6]
	return (data[0],close_price,data[2],open_price,high_price,low_price,price_change)


# 取得最新的歷史資料日期
def get_latest_data_date(company_num, db, db_cursor):
	query = ""
	if company_num == "":
		query = "select data_date from company_history_data ORDER BY data_date DESC LIMIT 1;"
	else:
		query = "select data_date from company_history_data where company_code=\""+company_num+"\" ORDER BY data_date DESC LIMIT 1;"
	db_cursor = db.cursor(dictionary=True)
	db_cursor.execute(query)
	result = db_cursor.fetchall()
	return result[0]["data_date"]

#儲存該公司的當月資料
def add_company_current_data(company_num, db, db_cursor):
	company_num = str(company_num)
	now = time.strftime('%Y-%m-%d %H:%M:%S')
	# db, db_cursor = connect_db(db_name="STOCK_INFO")
	try:
	# if 1:
		latest_data_date = get_latest_data_date(company_num, db, db_cursor)
		insert_datas = get_company_current_data(str(company_num),latest_data_date)
		# print(insert_data)
		for insert_data in insert_datas:
			if latest_data_date < insert_data[0]:	
			# if check_company_history_data(db,db_cursor,insert_data[0],company_num)==False:
				print(insert_data[0])
				insert_data = trans_raw_data(insert_data)
				query = "insert ignore into company_history_data (company_code,update_time,data_date,closing_price,volume,update_name,open_price,high_price,low_price) VALUES (\""+\
						str(company_num)+"\",\""+now+"\",\""+str(insert_data[0])+"\","+str(insert_data[1])+","+str(insert_data[2])+",\"py\","\
						+str(insert_data[3])+","+str(insert_data[4])+","+str(insert_data[5])+");"
				
				print(query)
				db_cursor.execute(query)
				query = "insert ignore into company_100_data (company_code,update_time,data_date,closing_price,volume,update_name,open_price,high_price,low_price) VALUES (\""+\
						str(company_num)+"\",\""+now+"\",\""+str(insert_data[0])+"\","+str(insert_data[1])+","+str(insert_data[2])+",\"py\","\
						+str(insert_data[3])+","+str(insert_data[4])+","+str(insert_data[5])+");"
				
				print(query)
				db_cursor.execute(query)
				# print(query.format(insert_data))
				# db.commit()
				insert_calculate_history_data(company_num, insert_data, db, db_cursor)
				# result = sorted(insert_data, key=lambda x: x[0], reverse=True)
				# if len(result)>0:
				# 	insert_calculate_history_data(company_num,result[0], db, db_cursor)
	except BaseException as error:
		write_error_log(error,company_num)
		pass

#判斷是否有該公司資料並儲存
def update_company_current_data(company_num, db, db_cursor):
	if check_company_data(company_num, db, db_cursor):
		add_company_current_data(company_num, db, db_cursor)
	else:
		add_company_history_data(company_num, db, db_cursor)

#main
#每天更新資料
def update_all_company_current_data():
	# create_error_file()
	all_company = []
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	try:
		all_company=get_all_company_num(db, db_cursor)
	except BaseException as error:
		write_error_log(error,"get_all_company_num fail")
	for company_num in all_company:
		print(company_num)

		# if int(company_num) != 1470:
		# 	continue
		
		write_log(company_num)

		# if 1:
		try:
			update_company_current_data(str(company_num).strip(), db, db_cursor)
			write_log("Success!")
		except BaseException as error:
			write_error_log(error,company_num)
			write_log("Fail!")
			pass
		db.commit()
	# db, db_cursor = connect_db(db_name="STOCK_INFO")
	qeury = "call STOCK_INFO.UpdateCompany100Data();"
	db_cursor.execute(qeury)
	db.commit()

#判斷是否有該公司資料並儲存2
def update_company_current_data_2(company_num, db, db_cursor):
	if check_company_data(company_num, db, db_cursor):
		add_company_current_data(company_num, db, db_cursor)
	else:
		add_company_history_data(company_num, db, db_cursor)

#main
#檢查資料
def update_all_company_current_data_2(start_date="",end_date="",check_day=-5, update=False):
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	now = datetime.now().strftime("%Y/%m/%d")
	now = datetime.strptime(now,"%Y/%m/%d")
	end = current_date = now
	if start_date=="":
		current_date = now + timedelta(days=check_day)
	else:
		if isinstance(start_date, datetime):
			current_date = start_date
		else:
			current_date = datetime.strptime(start_date, "%Y/%m/%d")
	if end_date!="":
		if isinstance(end_date, datetime):
			end = end_date
		else:
			end = datetime.strptime(end_date, "%Y/%m/%d")
	delta = timedelta(days=1)
	while current_date <= end:
		print(current_date)
		update_all_company_current_data_2_1(db, db_cursor, data_date=current_date, update=update)
		current_date += delta
		sleep(1)
	qeury = "call STOCK_INFO.UpdateCompany100Data();"
	db_cursor.execute(qeury)
	db.commit()

def update_all_company_current_data_2_1(db, db_cursor, data_date="", update=False):
	# twse_result = get_twse_company_data()
	if data_date=="":
		twse_result = get_twse_company_data_2()
		tpex_result = get_tpex_company_data()
		now_date = datetime.now().date()
	else:
		twse_result = get_twse_company_data_2(data_date.strftime("%Y%m%d"))
		tpex_result = get_tpex_company_data(str(data_date.year-1911)+data_date.strftime("/%m/%d"))
		now_date = data_date.date()

	result = {**twse_result, **tpex_result}
	all_company = []
	# db, db_cursor = connect_db(db_name="STOCK_INFO")
	try:
		all_company=get_all_company_num(db, db_cursor)
	except BaseException as error:
		write_error_log(error,"get_all_company_num fail")

	now = datetime.now()
	for company_num in all_company:
		if company_num in result:
			# latest_data_date = get_latest_data_date(company_num, db, db_cursor)
			# if latest_data_date < now:
			if check_company_history_data(db,db_cursor,now_date,company_num)==False:
				tmp = [now_date]+result[company_num]
				insert_data = trans_raw_data(tmp)
				print(tmp)


				print(insert_data)
				query = "insert ignore into company_history_data (company_code,update_time,data_date,closing_price,volume,update_name,open_price,high_price,low_price,price_change) VALUES (\""+\
						str(company_num)+"\",\""+str(now)+"\",\""+str(insert_data[0])+"\","+str(insert_data[1])+","+str(insert_data[2])+",\"py\","\
						+str(insert_data[3])+","+str(insert_data[4])+","+str(insert_data[5])+","+str(insert_data[6])+");"
						
				print(query)
				db_cursor.execute(query)
				query = "insert ignore into company_100_data (company_code,update_time,data_date,closing_price,volume,update_name,open_price,high_price,low_price,price_change) VALUES (\""+\
						str(company_num)+"\",\""+str(now)+"\",\""+str(insert_data[0])+"\","+str(insert_data[1])+","+str(insert_data[2])+",\"py\","\
						+str(insert_data[3])+","+str(insert_data[4])+","+str(insert_data[5])+","+str(insert_data[6])+");"
						
				
				print(query)
				db_cursor.execute(query)
						# print(query.format(insert_data))
						# db.commit()
				insert_calculate_history_data(company_num, insert_data, db, db_cursor)
			else:
				if update==True:
					tmp = [now_date]+result[company_num]
					insert_data = trans_raw_data(tmp)
					print(tmp)
					print(insert_data)
					# (data[0],close_price,data[2],open_price,high_price,low_price,price_change)
					query = '''
								update company_history_data set 
									update_time="{}"
									,
									closing_price={},
									volume={},
									update_name="py_update",
									open_price={},
									high_price={},
									low_price={},
									price_change={}
								where
									company_code="{}" and data_date="{}"
							'''
					query = query.format(str(now),str(insert_data[1]),str(insert_data[2]),str(insert_data[3]),str(insert_data[4]),str(insert_data[5]),str(insert_data[6]),str(company_num),str(insert_data[0]))
					print(query)
					db_cursor.execute(query)

					query = '''
								update company_100_data set 
									update_time="{}",
									closing_price={},
									volume={},
									update_name="py_update",
									open_price={},
									high_price={},
									low_price={},
									price_change={}
								where
									company_code="{}" and data_date="{}"
							'''
					query = query.format(str(now),str(insert_data[1]),str(insert_data[2]),str(insert_data[3]),str(insert_data[4]),str(insert_data[5]),str(insert_data[6]),str(company_num),str(insert_data[0]))
					db_cursor.execute(query)
					insert_calculate_history_data(company_num, insert_data, db, db_cursor)
	db.commit()

#檢查資料庫(company_history_data)是否有該公司資料
def check_company_data(company_num, db, db_cursor):
	company_num = str(company_num)
	# db, db_cursor = connect_db(db_name="STOCK_INFO")
	query = "select id from company_history_data where company_code=\""+company_num+"\";"
	db_cursor.execute(query)
	result = db_cursor.fetchall()
	if len(result)>0:
		return True
	else:
		return False

#get all company
def get_all_company_num(db, db_cursor):
	# db, db_cursor = connect_db(db_name="STOCK_INFO")
	query = "select company_code from company_id where alive=\"alive\" order by company_type, company_code;"
	db_cursor.execute(query)
	result = db_cursor.fetchall()
	all_company_num = []
	for row in result:
		all_company_num.append(row[0])
	return all_company_num

#插入新的資料到calculate_history_data
def insert_calculate_history_data(company_num, data, db, db_cursor):
	print(company_num,data)
	if check_calculate_history_data(company_num, db, db_cursor):
		query = "select * from company_history_calculate_data where company_code=\""+company_num+"\" order by data_date DESC LIMIT 1;"
		# db, db_cursor = connect_db(db_name="STOCK_INFO")
		db_cursor = db.cursor(dictionary=True)
		db_cursor.execute(query)
		result = db_cursor.fetchall()

		get_cp = get_history_data_from_now(db, db_cursor, company_num,101)
		first_closing_price = 0
		if len(get_cp)>0:
			first_closing_price = get_cp[0]["closing_price"]
		if first_closing_price is None:
			first_closing_price = 0

		get_v = get_history_data_from_now(db, db_cursor, company_num,21)
		first_volume = 0
		if len(get_v)>0:
			first_volume = get_v[0]["volume"]
		if first_volume is None:
			first_volume = 0

		get_latest_cp = get_history_data_from_now(db, db_cursor, company_num,2)
		latest_cp = 0
		if len(get_latest_cp)>0:
			latest_cp = get_latest_cp[0]["closing_price"]
		if latest_cp is None:
			latest_cp = 0

		get_5MA_cp = get_history_data_from_now(db, db_cursor, company_num,6)
		_5MA_cp = 0
		if len(get_5MA_cp)>0:
			_5MA_cp = get_5MA_cp[0]["closing_price"]
		if _5MA_cp is None:
			_5MA_cp = 0

		get_10MA_cp = get_history_data_from_now(db, db_cursor, company_num,11)
		_10MA_cp = 0
		if len(get_10MA_cp)>0:
			_10MA_cp = get_10MA_cp[0]["closing_price"]
		if _10MA_cp is None:
			_10MA_cp = 0

		current_closing_price = 0
		if data[1] is not None:
			current_closing_price = float(data[1])
		insert_closing_price = (current_closing_price - first_closing_price)/100 + result[0]["100MA"]
		if current_closing_price > insert_closing_price and current_closing_price > 10:
			insert_to_over_100MA(company_num,data[0], db, db_cursor)

		current_volume = 0
		if data[2] is not None:
			current_volume = float(data[2])
		insert_volume = (current_volume - first_volume)/20 + result[0]["monthly_avg_volume"]
		if current_volume!=0 and insert_volume != 0 and current_closing_price > 10:
			xtimes = current_volume/insert_volume
			if xtimes > 2:
				insert_to_monthly_avg_volume_over_2x(company_num,data[0],xtimes, db, db_cursor)

		gain_value = 0
		if latest_cp!=0 and current_closing_price!=0:
			gain_value = (current_closing_price - latest_cp)/latest_cp
			if gain_value > 0.035 and current_closing_price > 10:
				insert_to_gain_over_3_5(company_num,data[0],gain_value, db, db_cursor)
		print(latest_cp)

		insert_5MA = 0
		if _5MA_cp!=0 and current_closing_price!=0:
			insert_5MA = (current_closing_price - _5MA_cp)/5 + result[0]["5MA"]
		insert_10MA = 0
		if _10MA_cp!=0 and current_closing_price!=0:
			insert_10MA = (current_closing_price - _10MA_cp)/10 + result[0]["10MA"]

		if check_calculate_history_data(company_num, db, db_cursor,data_date=data[0])==False:
			query = '''insert ignore into company_history_calculate_data 
			(company_code,update_time,update_name,100MA,data_date,monthly_avg_volume,gain_percentage,5MA,10MA) Values ("'''+\
			company_num+'''","'''+str(datetime.now())+'''","py","'''+str(insert_closing_price)+'''","'''+\
			str(data[0])+'''","'''+str(insert_volume)+'''",'''+str(gain_value)+''','''+str(insert_5MA)+''','''+str(insert_10MA)+''')'''
			db_cursor.execute(query)
			print(query)
		else:
			query = '''
						update company_history_calculate_data set
							company_code="{}",
							update_time="{}",
							update_name="py",
							100MA="{}",
							data_date="{}",
							monthly_avg_volume="{}",
							gain_percentage={},
							5MA={},
							10MA={}
						WHERE 
							company_code="{}" and data_date="{}"
					'''
			query = query.format(company_num,str(datetime.now()),str(insert_closing_price),str(data[0]),str(insert_volume),str(gain_value),str(insert_5MA),str(insert_10MA),company_num,str(data[0]))

			db_cursor.execute(query)
			print(query)
		# db.commit()
	else:
		calculate_history_data(company_num, db, db_cursor)
	return

#檢查資料庫(company_history_calculate_data)是否有該公司資料
def check_calculate_history_data(company_num, db, db_cursor, data_date=""):
	company_num = str(company_num)
	# db, db_cursor = connect_db(db_name="STOCK_INFO")
	query = ""
	if data_date=="":
		query = "select id from company_history_calculate_data where company_code=\""+company_num+"\";"
	else:
		query = '''select id from company_history_calculate_data where company_code="{}" and data_date="{}";'''
		query = query.format(company_num,str(data_date))
	db_cursor.execute(query)
	result = db_cursor.fetchall()
	if len(result)>0:
		return True
	else:
		return False

#重新計算最新100日線、月均成交量
def recalculate():
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	latest_data_date = get_latest_data_date("", db, db_cursor)
	print(latest_data_date)
	delete_latest_company_history_calculate_data(db, db_cursor, latest_data_date)
	re_calculate_history_data(db, db_cursor)

def delete_latest_company_history_calculate_data(db, db_cursor, latest_data_date):
	query="delete from company_history_calculate_data where data_date=\""+str(latest_data_date)+"\";"
	print(query)
	db_cursor.execute(query)
	db.commit()

#重新計算(100日線、月均成交量)
def re_calculate_history_data(db="",db_cursor=""):
	if db == "" or db_cursor == "":
		db, db_cursor = connect_db(db_name="STOCK_INFO")
	all_num = get_all_company_num(db,db_cursor)
	for company_num in all_num:
		calculate_history_data(company_num, db, db_cursor, 105)
		# break
	db.commit()

#計算歷史資料(100日線、月均成交量)
def calculate_history_data(company_num, db, db_cursor, day_num="200"):
	query = "select * from company_history_data where company_code=\"%s\""
	with open("get_recent_260_data.sql","r") as f:
		query = f.read()
	db_cursor.execute(query.format(day_num,company_num))
	result = db_cursor.fetchall()
	if len(result) < 20:
		print("not much data to calculate")
		return
	i = 0
	volume_flag = 0
	volume_sum = 0
	closing_price_flag = 0
	closing_price_sum = 0
	_5MA_flag = 0
	_5MA_sum = 0
	_10MA_flag = 0
	_10MA_sum = 0
	last_closing_price = -1

	while i in range(len(result)):
		insert_volume = None
		insert_closing_price = None
		insert_5MA = None
		insert_10MA = None
		gain_percentage = None

		current_closing_price = result[i][2]
		if current_closing_price is None:
			current_closing_price = 0

		if result[i][3] != 0  and result[i][3] is not None:
			volume_sum += result[i][3]
		if result[i][2] != 0  and result[i][2] is not None:
			closing_price_sum += result[i][2]
			_5MA_sum += result[i][2]
			_10MA_sum += result[i][2]
			# print("last_data")
			# print(last_data)
			# last_data = get_last_data(db, db_cursor, company_num, non_zero=True, data_date=result[i][1])
			# if last_data!=0:
			if last_closing_price>0:
				# gain_percentage = (current_closing_price-last_data["closing_price"])/last_data["closing_price"]
				gain_percentage = (current_closing_price-last_closing_price)/last_closing_price
				print(gain_percentage)
			last_closing_price = result[i][2]
		if result[i] is None:
			break
		if i>=20:
			volume_flag=1
		if i>=100:
			closing_price_flag=1
		if i>=5:
			_5MA_flag=1
		if i>=10:
			_10MA_flag=1



		if volume_flag:
			if result[i-20][3] != 0  and result[i-20][3] is not None:
				volume_sum -= result[i-20][3]
			insert_volume = volume_sum/20
			xtimes = result[i][3]/insert_volume
			if xtimes > 2 and current_closing_price > 10:
				insert_to_monthly_avg_volume_over_2x(company_num,result[i][1],xtimes, db, db_cursor)

		if closing_price_flag:
			if result[i-100][2] != 0  and result[i-100][2] is not None:
				closing_price_sum -= result[i-100][2]
			insert_closing_price = closing_price_sum/100
			if current_closing_price > insert_closing_price and current_closing_price > 10:
				insert_to_over_100MA(company_num,result[i][1], db, db_cursor)

		if _5MA_flag:
			if result[i-5][2] != 0  and result[i-5][2] is not None:
				_5MA_sum -= result[i-5][2]
			insert_5MA = _5MA_sum/5
		if _10MA_flag:
			if result[i-10][2] != 0  and result[i-10][2] is not None:
				_10MA_sum -= result[i-10][2]
			insert_10MA = _10MA_sum/10

		print(result[i])

		print(i,insert_closing_price,insert_volume)
		if (insert_volume is not None) or (insert_closing_price is not None) or (insert_5MA is not None) or (insert_10MA is not None):
			if check_calculate_history_data(company_num,db,db_cursor,str(result[i][1]))==False:
				query = '''
							insert ignore into company_history_calculate_data 
							(company_code,update_time,update_name,100MA,data_date,monthly_avg_volume,5MA,10MA,gain_percentage) 
							Values ("{}","{}","py","{}","{}","{}","{}","{}","{}")'''
				query = query.format(company_num,str(datetime.now()),str(insert_closing_price),str(result[i][1]),str(insert_volume),str(insert_5MA),str(insert_10MA),str(gain_percentage))
				print(query)
				db_cursor.execute(query)
			# db.commit()
		# print(row)
		i+=1
		# if i>1:
		# 	break
	return

#not finish
#檢查資料庫中收盤價是否有0,null，改成和前日相同
def check_closing_price_0():
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	db_cursor = db.cursor(dictionary=True)
	query = "select * from company_history_data where closing_price is null;"
	db_cursor.execute(query)
	result = db_cursor.fetchall()
	with open("get_not_0_data.sql","r") as f:
		query = f.read()
	# print(query.format("123","456","789"))
	# data_date
	# company_code
	for row in result:
		print(row["company_code"])
		data_date = row["data_date"]
		company_code = row["company_code"]
		print(company_code,data_date)
		new_query = query.format(data_date,company_code,data_date)
		# print(new_query)
		db_cursor.execute(new_query)
		subresult = db_cursor.fetchall()
		if len(subresult)>0:
			last_date = subresult[0]["data_date"]
			print(subresult[0]["company_code"],subresult[0]["data_date"])
			new_query = "update company_history_data set"

# 取得最新的外資持股率歷史資料日期
def check_update_share_holding_ratio(company_num, db, db_cursor,data_date):
	query = "select data_date from company_history_data where company_code=\""+company_num+"\" and foreign_share_holding_ratio is null and data_date=\""+data_date.strftime("%Y/%m/%d")+"\";"
	# print(query)
	db_cursor = db.cursor(dictionary=True)
	db_cursor.execute(query)
	result = db_cursor.fetchall()
	if len(result)==0:
		return False
	return True

#main
#抓外資持股比率
def update_all_foreign_share_holding_ratio(start_date="",end_date="",check_day=-10):
	
	# driver = open_webdriver(url)
	# driver.implicitly_wait(15)
	# sleep(2)
	now = datetime.now().strftime("%Y/%m/%d")
	now = datetime.strptime(now,"%Y/%m/%d")
	end = current_date = now
	print(end)
	# current_date = now.strftime("%Y%m%d")
	# current_date = "20240121"
	# print(current_date)
	# params = {'date':current_date,'selectType':'ALLBUT0999','response':'json'}
	# r = requests.get(url, params=params, proxies=get_proxies())
	# print(r.text)
	# data = r.json()
	if start_date=="":
		current_date = now + timedelta(days=check_day)
	else:
		if isinstance(start_date, datetime):
			current_date = start_date
		else:
			current_date = datetime.strptime(start_date, "%Y/%m/%d")
	if end_date!="":
		if isinstance(end_date, datetime):
			end = end_date
		else:
			end = datetime.strptime(end_date, "%Y/%m/%d")
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	delta = timedelta(days=1)
	if not isinstance(check_day, int) or check_day<=0:
		check_day=-10
	while current_date <= end:
	# for i in range(check_day):
		# print(i)
		# current_date = now - timedelta(days=i)
		print(current_date)
		data = get_foreign_share_holding_ratio(current_date,"twse")
		update_foreign_share_holding_ratio(data,current_date,db,db_cursor,"twse")

		data = get_foreign_share_holding_ratio(current_date,"tpex")
		update_foreign_share_holding_ratio(data,current_date,db,db_cursor,"tpex")
		db.commit()
		sleep(2)
		current_date += delta
	# for d in data['data']:
	# 	print(d[0],d[7])
	# return result,date_time

def get_foreign_share_holding_ratio(data_date,cp_type,retry: int=5):
	twse_url = "https://www.twse.com.tw/rwd/zh/fund/MI_QFIIS"
	tpex_url = "https://www.tpex.org.tw/web/stock/3insti/qfii/qfii_result.php"
	for retry_i in range(retry):
		if cp_type=="twse":
			params = {'date':data_date.strftime("%Y%m%d"),'selectType':'ALLBUT0999','response':'json'}
			try:
				r = requests.get(twse_url, params=params, proxies=get_proxies())
				data = r.json()
				return data['data']
			except BaseException:
				continue

		elif cp_type=="tpex":
			params = {'date':data_date.strftime("%Y/%m/%d")}
			try:
				r = requests.get(tpex_url, params=params, proxies=get_proxies())
				data = r.json()
				return data['aaData']
			except BaseException:
				continue
	return []
	# return r.json()	

def update_foreign_share_holding_ratio(data,current_date,db,db_cursor,cp_type):
	if len(data) == 0:
		return
	for d in data:
		if cp_type=="twse":
			company_num = str(d[0])
		elif cp_type=="tpex":
			company_num = str(d[1])
		# query = "select "
		flag = check_update_share_holding_ratio(company_num,db,db_cursor,current_date)
		# latest_date = get_latest_share_holding_ratio_data_date(company_num,db,db_cursor)
		# print(latest_date)
		query1 = "update company_history_data SET foreign_share_holding_ratio="+str(d[7]).replace("%","")+" where company_code=\""+company_num+"\" and data_date=\""+current_date.strftime("%Y%m%d")+"\""
		query2 = "update company_100_data SET foreign_share_holding_ratio="+str(d[7]).replace("%","")+" where company_code=\""+company_num+"\" and data_date=\""+current_date.strftime("%Y%m%d")+"\""
		if flag:
			print(query1)
			db_cursor.execute(query1)
			db_cursor.execute(query2)
		# if isinstance(latest_date,datetime):
		# 	if latest_date < current_date:
		# 		print(query1)
		# 		db_cursor.execute(query1)
		# 		db_cursor.execute(query2)
		# else:
		# 	print(query1)
		# 	db_cursor.execute(query1)
		# 	db_cursor.execute(query2)
'''
def get_capital_amount_tw(company_num,driver):
	# url = "https://mops.twse.com.tw/mops/web/t05st03"
	# driver.get(url)
	# driver.implicitly_wait(15)
	print(company_num)
	textbox = driver.find_element(By.ID,"co_id")
	textbox.clear()
	# print(textbox)
	# textbox.clear()
	textbox.send_keys(company_num+Keys.ENTER)
	driver.implicitly_wait(15)
	# print(textbox.text)
	search_btn = driver.find_element(By.XPATH,"//*[@id=\"search_bar1\"]/div/input")
	search_btn.click()
	driver.implicitly_wait(15)
	time.sleep(5)
	# capital_amount = driver.find_element(By.XPATH,"//*[@id=\"table01\"]/table[2]/tbody/tr[9]/td[1]")
	# print(capital_amount.text)

	# Find all <tr> elements within the table
	all_tr_elements = driver.find_elements(By.XPATH,"//*[@id=\"table01\"]/table[2]/tbody/tr")

	# Loop through each <tr> element
	for tr_element in all_tr_elements:
		th_elements = tr_element.find_elements(By.XPATH,"th")
		# th_element = tr_element.find_element(By.XPATH,".//th[contains(text(), '實收資本額')]")
		# if th_element:
		# 	td_element = tr_element.find_element(By.XPATH,".//td")
		# 	print("實收資本額:", td_element.text)
		for th_element in th_elements:
			if "實收資本額" in th_element.text:
				# print("Found <th> element within <tr>:", th_element.text)
				# print("Parent <tr> text:", tr_element.text)
				td_element = tr_element.find_element(By.XPATH,"td")
				# print("capital_amount <td> text:", td_element.text)
				return td_element.text.replace("元","").strip()

# 爬資本額和發行量（慢）
def update_all_capital_amount_tw():
	# cService = webdriver.ChromeService(executable_path=driver_directory)
	# options = webdriver.ChromeOptions()
	# options.add_argument("--headless")
	# options.add_argument("--no-sandbox")
	# driver = webdriver.Chrome(service=cService, options=options)
	# url = "https://mops.twse.com.tw/mops/web/t05st03"
	# driver.get(url)
	driver = open_webdriver(url)
	driver.implicitly_wait(15)
	# sleep(1)
	# capital_amount = get_capital_amount_tw("1231",driver)
	# print(capital_amount)

	db, db_cursor = connect_db(db_name="STOCK_INFO")
	all_company = get_all_company_num(db,db_cursor)
	i=0
	# get_capital_amount_tw("1101",driver)
	for company_num in all_company:
		i+=1
		if int(company_num) < 2547:
			continue
		print(i)
		try:
			capital_amount = get_capital_amount_tw(company_num,driver)
		except Exception as error:
			capital_amount = get_capital_amount_tw(company_num,driver)
			time.sleep(1)
		print(capital_amount)
		query = "update company_id set capital_amount=\""+capital_amount+"\" where company_code=\""+company_num+"\""
		db_cursor.execute(query)
		db.commit()
		if i%2==0:
			time.sleep(5)
		if i%5==0:
			time.sleep(5)
		if i%100==0:
			time.sleep(60)
		# if i>100:
		# 	break
'''

# 爬資本額和發行量（快）
def update_all_capital_amount_tw_2():
	# cService = webdriver.ChromeService(executable_path=driver_directory)
	# options = webdriver.ChromeOptions()
	# options.binary_location = "/opt/google/chrome/chrome"
	# options.add_argument("--headless")
	# options.add_argument("--no-sandbox")
	# driver = webdriver.Chrome(service=cService, options=options)
	url = "https://mops.twse.com.tw/mops/web/t51sb01"
	# driver.get(url)
	driver = open_webdriver(url)
	driver.implicitly_wait(15)
	sleep(1)
	result = get_all_capital_amount_tw_2("上市",driver)
	print(len(result))
	result += get_all_capital_amount_tw_2("上櫃",driver)
	print(len(result))
	i=0
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	for data in result:
		i+=1
		query = "update company_id set capital_amount=\""+data[1]+"\", shares_issued=\""+data[2]+"\" where company_code=\""+data[0]+"\""
		
		print(data)
		print(query)
		db_cursor.execute(query)
		# if i>3:
		# 	break
	db.commit()
	
# 爬資本額和發行量（快）
def get_all_capital_amount_tw_2(type,driver):
	select_type = Select(driver.find_element(By.XPATH, "//*[@id=\"search\"]/table/tbody/tr/td/select[1]"))
	select_type.select_by_visible_text(str(type).strip())
	driver.implicitly_wait(15)
	sleep(2)
	select_code = Select(driver.find_element(By.XPATH, "//*[@id=\"search\"]/table/tbody/tr/td/select[2]"))
	select_code.select_by_visible_text("")
	driver.implicitly_wait(15)
	driver.find_element(By.XPATH,"//*[@id=\"search_bar1\"]/div/input").click()
	driver.implicitly_wait(15)
	sleep(5)

	content = driver.page_source
	root = etree.HTML(content)
	trs = root.xpath("//*[@id=\"table01\"]/table[2]/tbody/tr")[1:]

	result = []
	typ = ''
	i=0
	for tr in trs:
		i+=1
		tr = list(map(lambda x: x.text, tr.iter()))
		# print(tr[1],tr[2],tr[17],tr[18])
		if str(tr[1]).strip()=="公司":
			continue
		result.append((tr[1].strip(),tr[17].strip().replace(",",""),tr[18].strip().replace(",","")))
		# print(tr)
		# if i>16:
		# 	break
	# print(result)
	return result

# 打開web driver
def open_webdriver(url=""):
	cService = webdriver.ChromeService(executable_path=driver_directory)
	options = webdriver.ChromeOptions()
	if sys.platform.startswith('linux'): # 包含 linux 與 linux2 的情況
	    options.binary_location = "/opt/google/chrome/chrome"
	user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
	options.add_argument('--user-agent=%s' % user_agent)
	options.add_argument("--headless")
	options.add_argument("--no-sandbox")
	options.add_argument('--disable-extensions')
	driver = webdriver.Chrome(service=cService, options=options)
	driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
	  "source": """
	    Object.defineProperty(navigator, 'webdriver', {
	      get: () => undefined
	    })
	  """
	})
	if url != "":
		driver.get(url)
		driver.implicitly_wait(15)
	return driver

# 抓大戶持股
def ratio_crawl(retry:int=5):
    
    # 將網站回傳資料轉到 read_csv 解析，加入 headers 的功能為防止反爬蟲辨識，官方有時會擋 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_1\
    0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'} 
    
    # with open("/Users/lu-minchiang/Downloads/TDCC_OD_1-5.csv","r") as res:
	#     # df = pd.read_csv(StringIO(res.text))
    #     df = pd.read_csv(res)
    #     df = df.astype(str)
    #     df = df.rename(columns={
    #         '證券代號': 'stock_id',
    #         '股數': '持有股數', '占集保庫存數比例%': '占集保庫存數比例'
    #     })

    for i in range(retry):
    	try:
    	    res = requests.get("https://smart.tdcc.com.tw/opendata/getOD.ashx?id=1-5", headers=headers)
    	    df = pd.read_csv(StringIO(res.text))
    	    df = df.astype(str)
    	    df = df.rename(columns={
    	        '證券代號': 'stock_id',
    	        '股數': '持有股數', '占集保庫存數比例%': '占集保庫存數比例'
    	    })
    	    break
    	except BaseException:
    		continue
    
	    # 移除「公債」相關的id
    debt_id = list(set([i for i in df['stock_id'] if i[0] == 'Y']))
    df = df[~df['stock_id'].isin(debt_id)]
	    
	    # 官方有時會有不同格式誤傳，做例外處理
    if '占集保庫存數比例' not in df.columns:
        df = df.rename(columns={'佔集保庫存數比例%': '占集保庫存數比例'})
	        
	    # 持股分級=16時，資料都為0，要拿掉
    df = df[df['持股分級'] != '16']
	    
	    # 資料轉數字
    float_cols = ['人數', '持有股數', '占集保庫存數比例']
    df[float_cols] = df[float_cols].apply(lambda s: pd.to_numeric(s, errors="coerce"))
	    
	    # 抓表格上的時間資料做處理
    df['date'] = datetime.strptime(df[df.columns[0]][0], '%Y%m%d')
	    
	    #只要第二層欄位名稱
    df = df.drop(columns=df.columns[0])
	    
	    # 索引設置 unique index
    df = df.set_index(['stock_id', 'date', '持股分級'])
    return df

# 更新大戶持股
def update_holding_ratio():
	df = ratio_crawl()
	# print(df)
	insert_dic = {}
	for row in df.itertuples():
		# print(row)
		if row[0][2]=='12':
			insert_dic[row[0][0]] = [row[0][1],row[3]]
		if row[0][2]=='13' or row[0][2]=='14' or row[0][2]=='15':
			insert_dic[row[0][0]][1] += row[3]
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	all_num = get_all_company_num(db,db_cursor)
	for company_num in all_num:
		if company_num in insert_dic:
			data_date = insert_dic[company_num][0]
			ratio = insert_dic[company_num][1]
			print(company_num,data_date,ratio)
			query = "insert ignore into big_player_ratio (company_code,data_date,ratio,update_time,update_name) Values(\""+company_num+"\",\""+data_date.strftime("%Y%m%d")+"\","+str(ratio)+",\""+datetime.now().strftime("%Y%m%d")+"\",\"py\")"
			# query = "update big_player_ratio SET ratio="+str(ratio)+",update_time=\""+str(datetime.now())+"\" where company_code=\""+company_num+"\" and data_date=\""+data_date.strftime("%Y/%m/%d")+"\""
			print(query)
			db_cursor.execute(query)
	db.commit()

# 檢查company_history_data是否有此筆資料
def check_company_history_data(db,db_cursor,data_date,company_num):
	query = "select company_code from company_history_data where company_code=\""+company_num+"\" and data_date=\""+str(data_date)+"\""
	db_cursor.execute(query)
	result = db_cursor.fetchall()
	if len(result)>0:
		return True
	return False

#main
#更新每日盤後
def update_daily_company_data():
	# twse_result = get_twse_company_data()
	twse_result = get_twse_company_data_2()
	tpex_result = get_tpex_company_data()
	result = {**twse_result, **tpex_result}
	all_company = []
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	try:
		all_company=get_all_company_num(db, db_cursor)
	except BaseException as error:
		write_error_log(error,"get_all_company_num fail")
	now_date = datetime.now().date()
	now = datetime.now()
	for company_num in all_company:
		if company_num in result:
			# latest_data_date = get_latest_data_date(company_num, db, db_cursor)
			# if latest_data_date < now:
			if check_company_history_data(db,db_cursor,now_date,company_num)==False:
				tmp = [now_date]+result[company_num]
				insert_data = trans_raw_data(tmp)
				print(company_num)
				print(tmp)


				print(insert_data)
				query = "insert ignore into company_history_data (company_code,update_time,data_date,closing_price,volume,update_name,open_price,high_price,low_price,price_change) VALUES (\""+\
						str(company_num)+"\",\""+str(now)+"\",\""+str(insert_data[0])+"\","+str(insert_data[1])+","+str(insert_data[2])+",\"py\","\
						+str(insert_data[3])+","+str(insert_data[4])+","+str(insert_data[5])+","+str(insert_data[6])+");"
						
				print(query)
				db_cursor.execute(query)
				query = "insert ignore into company_100_data (company_code,update_time,data_date,closing_price,volume,update_name,open_price,high_price,low_price,price_change) VALUES (\""+\
						str(company_num)+"\",\""+str(now)+"\",\""+str(insert_data[0])+"\","+str(insert_data[1])+","+str(insert_data[2])+",\"py\","\
						+str(insert_data[3])+","+str(insert_data[4])+","+str(insert_data[5])+","+str(insert_data[6])+");"
						
				print(query)
				db_cursor.execute(query)
						# print(query.format(insert_data))
						# db.commit()
				insert_calculate_history_data(company_num, insert_data, db, db_cursor)
	db.commit()
	qeury = "call STOCK_INFO.UpdateCompany100Data();"
	db_cursor.execute(qeury)
	db.commit()

#上市盤後
def get_twse_company_data_2(target_date="",retry: int=5):
	if target_date=="":
		target_date = datetime.now().strftime("%Y%m%d")
	# 把 csv 檔抓下來
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_1\
    0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'} 
	url = f'https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?date={target_date}&type=ALL&response=json'
	# "fields":["證券代號","證券名稱","成交股數","成交筆數","成交金額","開盤價","最高價","最低價","收盤價","漲跌(+/-)",
	# "漲跌價差","最後揭示買價","最後揭示買量","最後揭示賣價","最後揭示賣量","本益比"]
	print(url)
	# url = "https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?date=20240126&type=ALL&response=json"
	for retry_i in range(retry):
		try:
			print(retry_i)
			res = requests.get(url, headers=headers)
			datas = res.json()
			# print("datas")
			# print(datas)
			print(res.headers.get('Content-Type', ''))
			if 'application/json' in res.headers.get('Content-Type', ''):
				print(res.headers.get('Content-Type', ''))
				break
			else:
				continue
			break
		except BaseException:
			continue
	i = 0
	result = {}
	if "tables" in datas:
		for data in datas["tables"]:
			# print(i)
			# print(len(data))
			i+=1
			
			if "title" in data:
				title = str(data["title"])
				if title.find("每日收盤行情(全部)")!=-1:
					# print(title)
					# print(data["fields"])
					post_data = data["data"]
					for d in post_data:
						d = list(map(lambda x:x.replace(",","").replace("--","0").replace('除息','Null').replace('除權','Null'),d))
						# print(d[0],d[8],d[2],d[5],d[6],d[7])
						symbols = re.findall(r'[+-]', d[9])
						# 收盤價,成交量,開盤價,最高價,最低價,漲跌
						if len(symbols)>0:
							result[d[0]]=[d[8],d[2],d[5],d[6],d[7],symbols[0]+d[10]]
						else:
							result[d[0]]=[d[8],d[2],d[5],d[6],d[7],d[10]]
	return result
#上市盤後（用csv較慢）
def get_twse_company_data(target_date=""):
	# 設定目標日期

	# target_date = '20230928'
	if target_date=="":
		target_date = datetime.now().strftime("%Y%m%d")
	# 把 csv 檔抓下來
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_1\
    0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'} 
	url = f'https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?date={target_date}&type=ALL&response=csv'
	res = requests.get(url, headers=headers)
	data = res.text 
	
	# 把爬下來的資料整理成需要的格式
	s_data = data.split('\n')
	output = []
	result = {}
	for d in s_data:
	    _d = d.split('","')
	    length = len(_d)
	    symbol = _d[0]
	  
	    if length == 16 and not symbol.startswith('='):
	        # output.append([
	        #   ele.replace('",\r','').replace('"','') 
	        #   for ele in _d
	        # ])
	        data=[]
	        data.append([
	          ele.replace('",\r','').replace('"','').replace('--','0').replace('\'','').replace(",","")
	          for ele in _d
	        ])
	        new_data = data[0]
	        output.append(new_data)
	        # print("data: ",new_data)
	        # 收盤價,成交量,開盤價,最高價,最低價
	        if len(new_data)>8:
		        print(new_data[0],new_data[8],str(new_data[2]).replace(",",""),new_data[5],new_data[6],new_data[7])
		        result[new_data[0]]=[new_data[8],str(new_data[2]).replace(",",""),new_data[5],new_data[6],new_data[7]]
	# print(output)

	# 轉成 DataFrame 並存成 csv 檔
	df = pd.DataFrame(output[1:], columns=output[0])
	df.set_index('證券代號', inplace=True)
	df.to_csv(f'stock_price_{target_date}.csv')
	return result

#上櫃盤後
def get_tpex_company_data(target_date="", retry: int=5):
	if target_date=="":
		now = datetime.now()
		target_date = str(now.year-1911)+now.strftime("/%m/%d")
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_1\
    0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'} 
	url = f"https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&o=htm&d={target_date}"
	# 	代號	名稱	收盤	漲跌	開盤	最高	最低	均價	成交股數	成交金額(元)	成交筆數	最後買價	最後買量(千股)	最後賣價	最後賣量(千股)	發行股數	
	#   次日參考價	次日漲停價	次日跌停價
	print(url)
	for retry_i in range(retry):
		try:
			res = requests.get(url, headers=headers)
			content = res.text
			break
		except BaseException:
			continue
	# res = requests.get(url, headers=headers)
	# content = res.text

	root = etree.HTML(content)
	# print(content)
	trs = root.xpath("//html/body/table/tbody/tr")[1:]

	result = {}
	typ = ''
	i=0
	# code,close,capacity,open,high,low,漲跌
	for tr in trs:
		i+=1
		tr = list(map(lambda x: x.text.replace('---','0').replace(",","").replace('\'','').replace('除息','Null').replace('除權','Null'), tr.iter()))
		if len(tr)>7:
			# print(tr[1],tr[3],str(tr[9]).replace(",",""),tr[5],tr[6],tr[7])
			result[tr[1]] = [tr[3],str(tr[9]).replace(",",""),tr[5],tr[6],tr[7],tr[4]]
		# print(tr[1],tr[2],tr[17],tr[18])
		# if str(tr[1]).strip()=="公司":
		# 	continue
		# result.append((tr[1].strip(),tr[17].strip(),tr[18].strip()))
	return result

#檢查給定月份是否有在區間內
def is_month_day_between(start_month_day, end_month_day, check_date):
    # 提取月和日
    check_month_day = (check_date.month, check_date.day)

    # 提取開始和結束的月和日
    start_month, start_day = start_month_day
    end_month, end_day = end_month_day

    # 判斷月和日是否在範圍內
    return (start_month, start_day) <= check_month_day <= (end_month, end_day)

#檢查finance_report是否有該資料
def check_finance_report(data):
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	query = '''
				select company_code from finance_report where company_code="{}" and year="{}" and season="{}"
			'''
	query = query.format(data[2],data[0],data[1])
	db_cursor.execute(query)
	result = db_cursor.fetchall()
	if len(result)>0:
		return True
	return False

#main
#更新EPS
def get_finance_report(year="",season=""):
	url = "https://mops.twse.com.tw/mops/web/t163sb04"
	# driver.get(url)
	driver = open_webdriver(url)
	driver.implicitly_wait(15)
	sleep(1)
	result = get_finance_report_data("上市",driver,year,season)
	print(len(result))
	result += get_finance_report_data("上櫃",driver,year,season)
	print(len(result))
	i=0
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	for data in result:
		if check_finance_report(data)==False:
			i+=1
			# query = "update company_id set capital_amount=\""+data[1]+"\", shares_issued=\""+data[2]+"\" where company_code=\""+data[0]+"\""
			query = '''
						insert ignore into finance_report
							(company_code,update_time,update_name,year,season,EPS) 
						VALUES
							("{}","{}","py","{}","{}","{}")
					'''
			query = query.format(data[2],str(datetime.now()),data[0],data[1],data[3])
			print(data)
			print(query)
			db_cursor.execute(query)
		# if i>3:
		# 	break
	db.commit()
	driver.quit()
	
# 爬EPS
def get_finance_report_data(type,driver,year="",season=""):

	now = datetime.now()
	# print(driver.find_element(By.XPATH, '''/html/body/center/table/tbody/tr/td/div[4]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div[3]/form/table/tbody/tr/td[2]/table/tbody/tr/td[3]/div/div/select''').id)
	# print(driver.find_element(By.ID, '''TYPEK''').id)
	select_type = Select(driver.find_element(By.XPATH, '''/html/body/center/table/tbody/tr/td/div[4]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div[3]/form/table/tbody/tr/td[2]/table/tbody/tr/td[3]/div/div/select'''))
	# select_type = Select(driver.find_element(By.ID, '''TYPEK'''))
	select_type.select_by_visible_text(str(type).strip())
	print(select_type.all_selected_options[0].text)
	driver.implicitly_wait(15)
	sleep(2)
	# year_box = driver.find_element(By.XPATH,"//input[@id='year']")
	year_box = driver.find_element(By.XPATH,'''/html/body/center/table/tbody/tr/td/div[4]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div[3]/form/table/tbody/tr/td[2]/table/tbody/tr/td[6]/div/div/input''')
	# print("year_box")
	# print(year_box.get_attribute("name"))
	# print(year_box.get_attribute("xpath"))
	# print(year_box.get_attribute("id"))
	# print(year_box)
	# year_box = driver.find_element(By.ID,"year")
	# year_box.send_keys(str(now.year-1911))
	# select_code = Select(driver.find_element(By.XPATH, "//*[@id=\"season\"]"))
	select_season = Select(driver.find_element(By.XPATH, '''/html/body/center/table/tbody/tr/td/div[4]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div[3]/form/table/tbody/tr/td[2]/table/tbody/tr/td[9]/div/div/select'''))
	
	if year=="" or season=="":
		year = 	str(now.year-1911)
		if is_month_day_between((3,31),(5,14),now):
			# year_box.send_keys(str(now.year-1911))
			# select_season.select_by_visible_text("1")
			season = "1"
		elif is_month_day_between((5,15),(8,13),now):
			# year_box.send_keys(str(now.year-1911))
			# select_season.select_by_visible_text("2")
			season = "2"
		elif is_month_day_between((8,14),(11,13),now):
			# year_box.send_keys(str(now.year-1911))
			# select_season.select_by_visible_text("3")
			season = "3"
		else:
			# print("season 4")
			if now.month < 6:
				# driver.execute_script("arguments[0].setAttribute('size', arguments[1]);", year_box, "5")
				# driver.execute_script("arguments[0].setAttribute('maxlength', arguments[1]);", year_box, "5")
				# driver.execute_script("arguments[0].setAttribute('value', arguments[1]);", year_box, str(now.year-1912).strip())
				# driver.execute_script("arguments[0].setAttribute('value', arguments[1]);", year_box, "111")
				# print(len(str(now.year-1912).strip()))
				year = str(now.year-1912).strip()
				# driver.execute_script("arguments[0].setAttribute('textbox', arguments[1]);", year_box, str(now.year-1912).strip())
				# driver.execute_script("arguments[0].setAttribute('innerHTML', arguments[1]);", year_box, str(now.year-1912).strip())
				# driver.execute_script("arguments[0].setAttribute('text', arguments[1]);", year_box, str(now.year-1912).strip())
				# year_box.send_keys(str(now.year-1912).strip())
			# else:
			# 	year_box.send_keys(str(now.year-1911).strip())
			# print(now.year-1912)
			# select_season.select_by_visible_text("4")
			season = "4"
			# select_season.select_by_visible_text("1")
	if float(year) > 1911:
		year = year-1911
	print(year,season)
	year_box.send_keys(str(year))
	select_season.select_by_visible_text(str(season))
	# year_box.submit()
	driver.implicitly_wait(15)
	# year_box = driver.find_element(By.XPATH,"//input[@id='year']")
	# year_box = driver.find_element(By.ID,"year")
	year_box = driver.find_element(By.XPATH,'''/html/body/center/table/tbody/tr/td/div[4]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div[3]/form/table/tbody/tr/td[2]/table/tbody/tr/td[6]/div/div/input''')
	# print(year_box.text)
	# print(year_box.get_attribute("innerHTML"))
	# print(year_box.get_attribute("textbox"))
	# print(year_box.get_attribute("value"))
	select_season = Select(driver.find_element(By.XPATH, '''/html/body/center/table/tbody/tr/td/div[4]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div[3]/form/table/tbody/tr/td[2]/table/tbody/tr/td[9]/div/div/select'''))
	print(select_season.all_selected_options[0].text)
	driver.implicitly_wait(15)

	# button = driver.find_element(By.XPATH,"//*[@id=\"search_bar1\"]/div/input")
	button = driver.find_element(By.XPATH,'''/html/body/center/table/tbody/tr/td/div[4]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div[3]/form/table/tbody/tr/td[4]/table/tbody/tr/td[2]/div/div/input''')
	button.click()
	# print(button.get_attribute("type"))
	# print(button.get_attribute("value"))
	# print(button.get_attribute("onclick"))
	driver.implicitly_wait(15)
	sleep(5)

	content = driver.page_source
	# with open("test.html","w") as f:
	# 	f.write(content)
	root = etree.HTML(content)
	# trs = root.xpath("//*[@id=\"table01\"]/table[2]/tbody/tr")[1:]
	tables = root.xpath("//*[@id=\"table01\"]/table")[0:]

	result = []
	typ = ''
	i=0
	for table in tables:
		trs = table.xpath(".//tbody/tr")[1:]
		print(len(trs))
		for tr in trs:
			i+=1
			tr = list(map(lambda x: x.text, tr.iter()))
			# print(tr)
			# print(tr[1],tr[2],tr[-1])

			# if str(tr[1]).strip()=="公司":
			# 	continue
			# result.append((tr[1].strip(),tr[17].strip().replace(",",""),tr[18].strip().replace(",","")))
			# year,season,company_code,eps
			result.append((round(float(year)+1911),season,tr[1],tr[-1]))
			# print(tr)
			# if i>3:
			# 	break
	# print(result)
	return result
