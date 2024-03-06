from get_data_lib import *
from DB import *
from email_lib import *
from fix_data import *
import datetime
# 更新上市，上櫃列表
import os
import sys

if sys.platform.startswith('linux'): # 包含 linux 與 linux2 的情況
    # Get the current working directory
    current_directory = os.getcwd()
    print("Current working directory:", current_directory)

    # Change the working directory to a new path
    new_directory = "/finance"
    os.chdir(new_directory)

    # Verify the change
    updated_directory = os.getcwd()
    print("Updated working directory:", updated_directory)
    print("Linux")
elif sys.platform.startswith('darwin'):
    print("MacOS")

arguments = sys.argv
args = {}
for arg in arguments:
    args[arg]=1




# if len(sys.argv)<2:
#     write_log("update_all_company_current_data")
#     update_all_company_current_data()

if len(sys.argv)>=2:
    if "company_data" in args:
        write_log("update_company_list")
        update_company_list()
        write_log("update_company_capital_amount")
        update_all_capital_amount_tw_2()
    if "fshr" in args:
        print("fshr")
        update_all_foreign_share_holding_ratio(check_day=-2)
    if "big_player_ratio" in args:
        print("big_player_ratio")
        update_holding_ratio()
    if "daily" in args:
        # write_log("update_company_list")
        # update_company_list()
        # write_log("update_company_capital_amount")
        # update_all_capital_amount_tw_2()
        print("daily")
        update_daily_company_data()
    # if "check_all" in args:
    #     print("check_all")
    #     write_log("update_company_list")
    #     update_company_list()
    #     write_log("update_company_capital_amount")
    #     update_all_capital_amount_tw_2()
    #     write_log("update_all_company_current_data")
    #     update_all_company_current_data()
    if "check_weekly" in args:
        print("check_all")
        # write_log("update_company_list")
        # update_company_list()
        # write_log("update_company_capital_amount")
        # update_all_capital_amount_tw_2()
        write_log("update_all_company_current_data")
        update_all_company_current_data_2(check_day=-6)
        update_all_foreign_share_holding_ratio(check_day=-6)
    if "recalculate" in args:
        print("recalculate")
        write_log("recalculate")
        recalculate()
        # calculate_5MA_10MA()
    if "get_finance_report" in args:
        print("get_finance_report")
        write_log("get_finance_report")
        get_finance_report()

# email_address = "bruce19960912@gmail.com"
# email_pwd = "qshxobuuxmsxddwp"
# filename = get_filter_3()
# send_from = email_address
# send_to = [email_address,"robinssss87@gmail.com","candy74316@gmail"]

# current_datetime = datetime.datetime.now()

# # Extract the current year and month
# current_year = current_datetime.year
# current_month = current_datetime.month
# current_day = current_datetime.day
# subject = str(current_year)+"/"+str(current_month)+"/"+str(current_day)+"挑選股票"
# message = "超過20週線、漲幅超過3.5%、超過月均成交量2倍"
# files = [filename]
# send_mail(send_from, send_to, subject, message, files=files,
#               server="smtp.gmail.com", port=587, username=email_address, password=email_pwd,
#               use_tls=True)
	
print("finish")