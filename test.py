from get_data_lib import *
from DB import *
from email_lib import *
from fix_data import *
# get_filter_3()

email_address = "bruce19960912@gmail.com"
email_pwd = "qshxobuuxmsxddwp"
# path = "/Users/lu-minchiang/Desktop/finance/result/filter_3/2024/1/2024-1-6_filter_3"
# send_mail(send_from = email_address, send_to = email_address, subject = "test sub", message = "test msg", files=["/Users/lu-minchiang/Desktop/finance/result/filter_3/2024/1/2024-1-6_filter_3"],
#               server="smtp.google.com", port=587, username=email_address, password='luminchiang',
#               use_tls=True)

# #import get_data_lib

# get_company_data()


# get_company_data()

# save_company_data()
# add_company_data(1342)


# all_company=get_all_company_num()
# for num in all_company:
# 	print(num)
# update_all_company_current_data()
# get_capital_amount(1101)
# update_company_list()
# TWSE_EQUITIES_URL = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
# TPEX_EQUITIES_URL = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=4'
# def get_directory():
#     return os.path.dirname(os.path.abspath(__file__))
# to_csv(TWSE_EQUITIES_URL, os.path.join(get_directory(), 'twse_equities.csv'))
# to_csv(TPEX_EQUITIES_URL, os.path.join(get_directory(), 'tpex_equities.csv'))
# all_code = []
# for code in twstock.codes:
# 	# print(code)
# 	if twstock.codes[code].type == "股票":
# 		print(code)
# 		print(twstock.codes[code])

# update_all_company_current_data()

# result,date_time = get_foreign_share_holding_ratio()
# print(date_time)
# for key in result:
# 	print(key, result[key])
# update_company_list()



# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders

# # Set your email credentials and details
# sender_email = email_address
# receiver_email = email_address
# subject = "Email with Attachment"
# body = "This is the body of the email."

# # Create a MIME object to represent the email message
# message = MIMEMultipart()
# message["From"] = sender_email
# message["To"] = receiver_email
# message["Subject"] = subject
# message.attach(MIMEText(body, "plain"))

# # Attach the file to the email
# file_path = path
# attachment = open(file_path, "rb")
# part = MIMEBase("application", "octet-stream")
# part.set_payload(attachment.read())
# encoders.encode_base64(part)
# file_name = "2024-1-6_filter_3.txt"
# part.add_header("Content-Disposition", f"attachment; filename= {file_name}")
# message.attach(part)

# # Connect to the SMTP server (e.g., Gmail)
# smtp_server = "smtp.gmail.com"
# smtp_port = 587
# smtp_username = email_address
# smtp_password = email_pwd
# print("sending email")
# with smtplib.SMTP(smtp_server, smtp_port) as server:
#     # Start the TLS connection (for secure connections)
#     server.starttls()

#     # Login to your email account
#     server.login(smtp_username, smtp_password)

#     # Send the email
#     server.sendmail(sender_email, receiver_email, message.as_string())
# result = get_history_data_from_now(company_num="1101", day_num=100, non_zero=False)
# all_company = get_all_company_num()
# for cp_num in all_company:
# 	print(cp_num)
# 	calculate_history_data(cp_num)
# result = calculate_history_data("1101")
# print(result)


# current_directory = os.getcwd()
# current_datetime = datetime.
# datetime.now()
# current_year = current_datetime.year
# current_month = current_datetime.month
# current_day = current_datetime.day
# error_log_name = "/error_log/"+str(current_year)+"/"+str(current_month)+"/"+str(current_year)+"-"+str(current_month)+"-"+str(current_day)+"_error_log"
# print(current_directory)
# filename = current_directory+error_log_name
# print(filename)
# os.makedirs(os.path.dirname(filename), exist_ok=True)
# print(filename)
# with open(filename, "a") as f:
# 	f.write(str(msg))
# 	f.write(str(error))
# 	f.write("\n##########################\n")
# write_error_log(ValueError,"test")
# print(type(datetime.datetime.now()))

# cp =["2740","5016","6287","6462","8455","8923"]
# db, db_cursor = connect_db(db_name="STOCK_INFO")
# for cp_num in cp:
# 	update_company_current_data(cp_num.strip(), db, db_cursor)
# add_company_history_data("1795", db, db_cursor)
# db.commit()
# data_date = get_latest_data_date("1101", db, db_cursor)
# print(data_date)
# print(type(data_date))
# insert_data = get_company_current_data("1101",data_date)
# print(str(insert_data[0][0]))
# write_log("test")
# initial_all_company_history_data()
# import os

# # Get the current working directory
# current_directory = os.getcwd()
# print("Current working directory:", current_directory)

# # Change the working directory to a new path
# new_directory = "/"
# os.chdir(new_directory)

# # Verify the change
# updated_directory = os.getcwd()
# print("Updated working directory:", updated_directory)
# for cp_num in cp:
# 	update_company_current_data(cp_num.strip(), db, db_cursor)
# insert_datas = get_company_history_data("1435")
# sub_insert_data("1435", insert_datas, db, db_cursor)
# db.commit()
# update_all_capital_amount_tw()
# update_all_capital_amount_tw_2()
# update_all_foreign_share_holding_ratio()

# df = ratio_crawl()
# print(type(df))
# print(df.index)
# print(df.dtypes)
# print(df['人數'])
# df_list = df.values.tolist()

# # print(df_list)
# # for i in range(len(df.index)):
# # 	# print(df.index[i],df_list[i])
# # 	print(df.index[i],df.values[i])
# print(df)
# insert_data = []
# insert_dic = {}
# for row in df.itertuples():
# 	if row[0][2]=='15':
# 		# print(row)
# 		# print(row[0],row[3])
# 		insert_dic[row[0][0]] = [row[0][1],row[3]]
# 		insert_data.append([row[0],row[3]])
# print(len(df.index))
# print(len(insert_data))
# print(insert_dic)
# update_holding_ratio()
# get_tpex_company_data()
# get_twse_company_data()
# update_daily_company_data()
# all_num = get_company_num
# re_calculate_history_data()
# calculate_history_data("9960", db, db_cursor)
# get_twse_company_data_2()
# calculate_5MA_10MA()
# url = "https://mops.twse.com.tw/mops/web/t163sb04"
# driver = open_webdriver(url)
# driver.implicitly_wait(15)
# sleep(1)
# get_finance_report_2("上市",driver)
# driver.quit()
# get_finance_report(112,1)
# get_finance_report(112,2)
# get_finance_report(111,4)
# result = get_last_data(db, db_cursor, company_num="1101", non_zero=True, data_date="")
# print(result)
# db, db_cursor = connect_db(db_name="STOCK_INFO")
complete_calculate_gain_percentage(100)
print("finish")






