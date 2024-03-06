from django.shortcuts import render, redirect
from .models import *
from locallibrary.models import Company100Data, CompanyHistoryData, CompanyId, GainOver35, MonthlyAvgVolumeOver2X, Over100Ma, BigPlayerRatio
import datetime
from .lib.lib import *
from django.utils import timezone
from django.http import HttpResponse
import pytz
# Create your views here.


def my_view(request):
	data_from_view = Filter3.objects.all().order_by('company_type','company_code')
	# print(type(data_from_view))
	company_data = []
	# latest_company_data = []
	# latest_date = 
	# Create a specific datetime object with a time zone
	# latest_date = timezone.make_aware(datetime.datetime.now() + datetime.timedelta(days=-10), timezone=timezone.utc)
	latest_date = timezone.now()+ datetime.timedelta(days=-10)
	for obj in data_from_view:
		everyday_data = Company100Data.objects.filter(company_code=obj.company_code).order_by('-data_date')
		latest_data = everyday_data.latest('data_date')
		
		# latest_data = everyday_data.first()
		if latest_date < latest_data.data_date:
			latest_date = latest_data.data_date
		for one_day_data in everyday_data:
			one_day_data.data_date = trans_date_to_milli_timestamp(one_day_data.data_date)
		pair_data = [obj,latest_data,everyday_data]
		# pair_latest_data = [obj.company_code,latest_data]
		company_data.append(pair_data)
		# latest_company_data.append(pair_latest_data)
	select_data_date = Company100Data.objects.all().latest("data_date").data_date
	result = get_from_db(select_data_date)
	# print(result)
	# for row in result:
	select_date = Company100Data.objects.order_by('-data_date').values('data_date').distinct()
	select_option=[]
	for i in range(len(select_date)):
		# print(select_date[i])
		tmp=select_date[i]["data_date"].strftime("%Y/%m/%d")
		select_option.append(tmp)
		# print(tmp)

	return render(request, 'catalog/test.html', {'data_from_view': data_from_view
		,'company_data': company_data,'latest_date': latest_date
		,'overlap': result
		,'select_date': select_option
		})


def show_stocks(request):
	# select_option=get_date()
	print(request.method)
	if request.method =='POST':
		print("click")
		# my_view(request)
		print(request.POST)
		button_clicked = request.POST['button']
		print(button_clicked)
		datepicker = request.POST.get('datepicker', None)

		#price_volume
		price_volume_check = 'on'
		price_volume_check = request.POST.get('price_volume_check', 'off')
		print('price_volume_check')
		print(price_volume_check)
		volume_threshold = 2000
		volume_threshold = request.POST.get('volume_threshold', "2000")
		print('volume_threshold')
		print(volume_threshold)
		if is_num(volume_threshold):
			print("is digit")
			volume_threshold = float(volume_threshold)
		else:
			volume_threshold = 2000
		print(volume_threshold)
		gain_percentage_threshold = 3.5
		gain_percentage_threshold = request.POST.get('gain_percentage_threshold', "3.5")
		print('gain_percentage_threshold')
		print(gain_percentage_threshold)
		if is_num(gain_percentage_threshold):
			print("is digit")
			gain_percentage_threshold = float(gain_percentage_threshold)
		else:
			gain_percentage_threshold = 3.5
		print(gain_percentage_threshold)
		#fshr
		fshr_check = 'off'
		fshr_check = request.POST.get('fshr_check', 'off')
		print('fshr_check')
		print(fshr_check)
		fshr_gain_threshold = 5
		fshr_gain_threshold = request.POST.get('fshr_gain_threshold', "5")
		print('fshr_gain_threshold')
		print(fshr_gain_threshold)
		if is_num(fshr_gain_threshold):
			print("is digit")
			fshr_gain_threshold = float(fshr_gain_threshold)
		else:
			fshr_gain_threshold = 5
		print(fshr_gain_threshold)
		fshr_culmulate_day = 5
		fshr_culmulate_day = request.POST.get('fshr_culmulate_day', "5")
		print('fshr_culmulate_day')
		print(fshr_culmulate_day)
		if is_num(fshr_culmulate_day):
			print("is digit")
			fshr_culmulate_day = float(fshr_culmulate_day)
			fshr_culmulate_day = round(fshr_culmulate_day)
		else:
			fshr_culmulate_day = 5
		print(fshr_culmulate_day)
		fshr_data = [fshr_check,fshr_gain_threshold,fshr_culmulate_day]
		#big_player
		big_player_check = "on"
		big_player_check = request.POST.get('big_player_check', "off")
		big_player_threshold = 50
		big_player_threshold = request.POST.get('big_player_threshold', "0")
		print("big_player_threshold")
		print(big_player_threshold)
		if is_num(big_player_threshold):
			print("is digit")
			big_player_threshold = float(big_player_threshold)
		else:
			big_player_threshold = 50
		big_player_data = [big_player_check, big_player_threshold]

		if price_volume_check == "off" and fshr_check == "off":
			price_volume_check = "on"
		price_volume_data = [price_volume_check,volume_threshold,gain_percentage_threshold]
		print("price_volume_check")
		print(price_volume_check)
		print("fshr_check")
		print(fshr_check)
		# print("datepicker")
		# print(datepicker)
		if datepicker is not None and datepicker != "":
			print("datepicker: "+datepicker)
			datepicker = datepicker.replace("-","/")
			naive_datetime = datetime.datetime.strptime(datepicker, "%Y/%m/%d")
			select_data_date = Company100Data.objects.filter(data_date__lte=naive_datetime).latest("data_date").data_date
			print(select_data_date)
			# company_data,latest_date,select_option = render_show_stocks(request,select_data_date,price_volume_data,fshr_data)
			company_data,latest_date = render_show_stocks(request,select_data_date,price_volume_data,fshr_data,big_player_data)
		else:
			select_data_date = Company100Data.objects.all().latest("data_date").data_date
			# company_data,latest_date,select_option = render_show_stocks(request,select_data_date,price_volume_data,fshr_data)
			company_data,latest_date = render_show_stocks(request,select_data_date,price_volume_data,fshr_data,big_player_data)
		# selected_value = request.POST.get('dropdown', None)
		# if selected_value:
		# 	print(selected_value)
		# 	naive_datetime = datetime.datetime.strptime(selected_value, "%Y/%m/%d")
		# 	company_data,latest_date,company_data,select_option = render_show_stocks(request,naive_datetime)
	else:
		select_data_date = Company100Data.objects.all().latest("data_date").data_date
		price_volume_data = ['on',2000,3.5]
		fshr_data = ['off',5,5]
		big_player_data = ['on',50]
		# company_data,latest_date,select_option = render_show_stocks(request,select_data_date,price_volume_data,fshr_data)
		company_data,latest_date = render_show_stocks(request,select_data_date,price_volume_data,fshr_data,big_player_data)
	# result = get_from_db(select_data_date)

	# # data_from_view = Filter3.objects.all().order_by('company_type','company_code')
	# all_company_name = CompanyId.objects.all()
	# company_data = []
	# latest_date = timezone.now()+ datetime.timedelta(days=-10)

	# for obj in result:
	# 	everyday_data = Company100Data.objects.filter(company_code=obj["company_code"]).order_by('data_date')
	# 	# latest_data = Company100Data.objects.filter(company_code=obj.company_code).order_by('-data_date').latest('data_date')
	# 	latest_data = everyday_data.latest('data_date')
	# 	# latest_data = everyday_data.first()

	# 	if latest_date < latest_data.data_date:
	# 		latest_date = latest_data.data_date
	# 	last_closing_price = 0
	# 	for one_day_data in everyday_data:
	# 		if one_day_data.closing_price is None:
	# 			one_day_data.closing_price = last_closing_price
	# 			one_day_data.open_price = last_closing_price
	# 			one_day_data.high_price = last_closing_price
	# 			one_day_data.low_price = last_closing_price
	# 		last_closing_price = one_day_data.closing_price
	# 		one_day_data.volume = one_day_data.volume/1000
	# 		one_day_data.data_date = trans_date_to_milli_timestamp(one_day_data.data_date)

	# 	company_name = all_company_name.filter(company_code=obj["company_code"])
	# 	shares_issued = int(company_name[0].shares_issued.replace(",",""))/1000
	# 	# obj.latest_volume = obj.latest_volume/1000
	# 	latest_data.volume = latest_data.volume/1000

	# 	latest_big_player_ratio = BigPlayerRatio.objects.filter(company_code=obj["company_code"]).order_by('data_date').latest('data_date')
	# 	pair_data = [obj, latest_data, latest_big_player_ratio.ratio, company_name[0].company_name, shares_issued, everyday_data]
	# 	company_data.append(pair_data)
	return render(request, 'catalog/show_stocks.html', {'company_data': company_data
		,'latest_date': latest_date.strftime("%Y-%m-%d")
		,'company_number': len(company_data)
		,'price_volume_data': price_volume_data
		,'fshr_data': fshr_data
		,'big_player_data': big_player_data
		# ,'select_date': select_option
		})


def render_show_stocks(request,data_date,price_volume_data=[],fshr_data=[],big_player_data=[]):
	# select_option=get_date()

	# naive_datetime = datetime.datetime.strptime(selected_value, "%Y/%m/%d")
	result = []
	result1 = []
	# result1 = get_from_db(data_date)
	result2 = []
	if price_volume_data[0]=="on":
		result1 = get_by_filter_price_volume(data_date, price_volume_data[1], price_volume_data[2])
		result = result1
	if fshr_data[0]=="on":
		result2 = get_by_filter_fshr_gain(data_date, fshr_data[1], fshr_data[2])
		result = result2
	if price_volume_data[0]=="on" and fshr_data[0]=="on":
		set1 = set(item['company_code'] for item in result1)
		set2 = set(item['company_code'] for item in result2)

		# 找到兩個集合的交集
		intersection_set = set1.intersection(set2)
		print("#######################")
		print(len(set1))
		print(set1)
		print(len(set2))
		print(set2)
		print(intersection_set)
		print(len(intersection_set))
		print("#######################")
		result = intersection_set
		result = [{'company_code':d} for d in result]

	# if big_player_data[0]=="on":
	# 	result3 = get_by_filter_big_player(data_date,big_player_data[1])
	# 	set3 = set(item['company_code'] for item in result3)
	# 	intersection_set = intersection_set.intersection(set3)

	# result = result1
	
	# select_data_date = Company100Data.objects.all().latest("data_date").data_date
	# result = get_from_db(select_data_date)

	# data_from_view = Filter3.objects.all().order_by('company_type','company_code')
	all_company_name = CompanyId.objects.all()
	company_data = []
	# if data_date.tzinfo is None:
	# 	timezone = pytz.timezone('UTC')
	# 	latest_date = timezone.localize(data_date)+ datetime.timedelta(days=-10)
	# else:
	# 	latest_date = data_date+ datetime.timedelta(days=-10)
	# latest_date = timezone.now()+ datetime.timedelta(days=-10)

	for obj in result:
		print(obj)
		latest_big_player_ratio = BigPlayerRatio.objects.filter(company_code=obj['company_code']).order_by('data_date').latest('data_date')
		if big_player_data[0]=="on":
			if latest_big_player_ratio.ratio < big_player_data[1]:
				continue
		# everyday_data = Company100Data.objects.filter(company_code=obj["company_code"]).order_by('data_date')
		everyday_data = get_everyday_data(obj["company_code"])
		# latest_data = Company100Data.objects.filter(company_code=obj.company_code).order_by('-data_date').latest('data_date')
		# latest_data = everyday_data.latest('data_date')
		latest_data = everyday_data[-1]
		# print(latest_data.price_change)
		# if latest_data["volume"] < 2000000:
		# 	continue
		# latest_data = everyday_data.first()

		# if latest_date < latest_data.data_date:
		# 	latest_date = latest_data.data_date
		last_closing_price = 0
		for one_day_data in everyday_data:
			if one_day_data["gain_percentage"] is not None:
				one_day_data["gain_percentage"] *= 100
				one_day_data["gain_percentage"] = round(one_day_data["gain_percentage"],2)
			if one_day_data["closing_price"] is None:
				one_day_data["closing_price"] = last_closing_price
				one_day_data["open_price"] = last_closing_price
				one_day_data["high_price"] = last_closing_price
				one_day_data["low_price"] = last_closing_price
			last_closing_price = one_day_data["closing_price"]
			one_day_data["volume"] = round(one_day_data["volume"]/1000,3)
			one_day_data["data_date"] = trans_date_to_milli_timestamp(one_day_data["data_date"])

		company_name = all_company_name.filter(company_code=obj["company_code"])
		shares_issued = int(company_name[0].shares_issued.replace(",",""))/1000
		# obj.latest_volume = obj.latest_volume/1000
		# latest_data["volume"] = latest_data["volume"]/1000
		finance_report = get_finance_report(obj["company_code"])
		# latest_big_player_ratio = BigPlayerRatio.objects.filter(company_code=obj["company_code"]).order_by('data_date').latest('data_date')
		pair_data = [obj, latest_data, latest_big_player_ratio.ratio, company_name[0].company_name, shares_issued, finance_report, everyday_data]
		company_data.append(pair_data)
	# return company_data,data_date,select_option
	return company_data,data_date

	# return render(request, 'catalog/show_stocks.html', {'company_data': company_data
	# 	,'latest_date': data_date.strftime("%Y/%m/%d")
	# 	# ,'latest_date': selected_value
	# 	,'company_number': len(company_data)
	# 	,'select_date': select_option
	# 	})

def button_click_view(request):
	if request.method =='POST':
		print("click")
		# my_view(request)
		selected_value = request.POST.get('dropdown', None)
		if selected_value:
			print(selected_value)
			naive_datetime = datetime.datetime.strptime(selected_value, "%Y/%m/%d")
			company_data,data_date,company_data,select_option = render_show_stocks(request,naive_datetime)
			# result = get_from_db(datetime.datetime.strptime(selected_value, "%Y/%m/%d"))

			# # data_from_view = Filter3.objects.all().order_by('company_type','company_code')
			# all_company_name = CompanyId.objects.all()
			# company_data = []
			# import pytz
			# timezone = pytz.timezone('UTC')
			# latest_date = timezone.localize(naive_datetime)+ datetime.timedelta(days=-10)

			# for obj in result:
			# 	everyday_data = Company100Data.objects.filter(company_code=obj["company_code"]).order_by('data_date')
			# 	# latest_data = Company100Data.objects.filter(company_code=obj.company_code).order_by('-data_date').latest('data_date')
			# 	latest_data = everyday_data.latest('data_date')
			# 	# latest_data = everyday_data.first()

			# 	if latest_date < latest_data.data_date:
			# 		latest_date = latest_data.data_date
			# 	last_closing_price = 0
			# 	for one_day_data in everyday_data:
			# 		if one_day_data.closing_price is None:
			# 			one_day_data.closing_price = last_closing_price
			# 			one_day_data.open_price = last_closing_price
			# 			one_day_data.high_price = last_closing_price
			# 			one_day_data.low_price = last_closing_price
			# 		last_closing_price = one_day_data.closing_price
			# 		one_day_data.volume = one_day_data.volume/1000
			# 		one_day_data.data_date = trans_date_to_milli_timestamp(one_day_data.data_date)

			# 	company_name = all_company_name.filter(company_code=obj["company_code"])
			# 	shares_issued = int(company_name[0].shares_issued.replace(",",""))/1000
			# 	# obj.latest_volume = obj.latest_volume/1000
			# 	latest_data.volume = latest_data.volume/1000

			# 	latest_big_player_ratio = BigPlayerRatio.objects.filter(company_code=obj["company_code"]).order_by('data_date').latest('data_date')
			# 	pair_data = [obj, latest_data, latest_big_player_ratio.ratio, company_name[0].company_name, shares_issued, everyday_data]
			# 	company_data.append(pair_data)
			return render(request, 'catalog/show_stocks.html', {'company_data': company_data
				# ,'latest_date': latest_date.strftime("%Y/%m/%d")
				,'latest_date': selected_value
				,'company_number': len(company_data)
				,'select_date': select_option
				})
		# return 
		# return redirect('./templates/catalog/test.html')
	return
	# return render(request, 'catalog/test.html')

def test2(request):
	# company_data = []
	all_company_name = CompanyId.objects.all()
	everyday_data = Company100Data.objects.filter(company_code="1101").order_by('data_date')
		# latest_data = Company100Data.objects.filter(company_code=obj.company_code).order_by('-data_date').latest('data_date')
	latest_data = everyday_data.latest('data_date')
		# latest_data = everyday_data.first()
	latest_date = timezone.now()+ datetime.timedelta(days=-10)
	if latest_date < latest_data.data_date:
		latest_date = latest_data.data_date
	last_closing_price = 0
	for one_day_data in everyday_data:
		if one_day_data.closing_price is None:
			one_day_data.closing_price = last_closing_price
		last_closing_price = one_day_data.closing_price
		one_day_data.volume = one_day_data.volume/1000
		one_day_data.data_date = trans_date_to_milli_timestamp(one_day_data.data_date)
	company_name = all_company_name.filter(company_code="1101")
	# obj.latest_volume = obj.latest_volume/1000
	latest_data.volume = latest_data.volume/1000
	pair_data = ["1101", latest_data, company_name[0].company_name, everyday_data]
	print(latest_data)
	print(company_name)
	print(everyday_data)
	# company_data.append(pair_data)
	return render(request, 'catalog/test2.html', {'latest_data': latest_data, 'company_name': company_name, 'everyday_data': everyday_data
		,'latest_date': latest_date.strftime("%Y/%m/%d")
		})




