import datetime
from .DB import *
from locallibrary.models import Company100Data, CompanyHistoryData, CompanyId, GainOver35, MonthlyAvgVolumeOver2X, Over100Ma, BigPlayerRatio

# Create your views here.

def is_num(a):
	try:
		float(a)
		return True
	except:
		return False

def get_everyday_data(company_code):
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	db_cursor = db.cursor(dictionary=True)
	query = '''select
				c1.company_code,
				c1.data_date,
				c1.closing_price,
				c1.open_price,
				c1.high_price,
				c1.low_price,
				c1.volume,
				c1.foreign_share_holding_ratio,
				c1.price_change,
				c2.100MA,
				c2.monthly_avg_volume,
				c2.gain_percentage,
				c2.5MA,
				c2.10MA
			FROM company_100_data c1
			LEFT JOIN
				company_history_calculate_data c2 ON c1.company_code=c2.company_code and c1.data_date=c2.data_date
			WHERE c1.company_code="'''+company_code+'''" order by c1.data_date'''
	# everyday_data = Company100Data.objects.filter(company_code=obj["company_code"]).order_by('data_date')
	db_cursor.execute(query)
	result = db_cursor.fetchall()
	# print("###########################")
	# print(result[0])
	# print(query)
	return result


def trans_date_to_milli_timestamp(date_time):
	tmp_time = date_time.strftime("%Y-%m-%d")
	# print(tmp_time)
	tmp_time = datetime.datetime.strptime(tmp_time,"%Y-%m-%d")
	# print(tmp_time)
	return tmp_time.timestamp()*1000

def get_from_db(data_time):
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	db_cursor = db.cursor(dictionary=True)
	query = "SELECT\
			    g.company_code,\
			    g.data_date,\
			    g.gain_value\
			FROM\
			    gain_over_3_5 g\
			INNER JOIN\
			    monthly_avg_volume_over_2x m ON g.company_code = m.company_code AND g.data_date = m.data_date\
			INNER JOIN\
			    over_100MA o ON g.company_code = o.company_code AND g.data_date = o.data_date\
			WHERE g.data_date = \""+str(data_time.strftime('%Y-%m-%d'))+"\";"

	db_cursor.execute(query)
	result = db_cursor.fetchall()
	# print(query)
	return result



def get_by_filter_price_volume(data_date, volume_threshold=2000, price_gain_threshold=3.5):
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	db_cursor = db.cursor(dictionary=True)
	query = '''
				select
				c1.company_code,
				c1.data_date,
				c1.closing_price
			FROM company_100_data c1
			INNER JOIN
			    monthly_avg_volume_over_2x m ON c1.company_code = m.company_code AND c1.data_date = m.data_date
			INNER JOIN
				over_100MA o ON c1.company_code = o.company_code AND c1.data_date = o.data_date
			LEFT JOIN
				company_history_calculate_data c2 ON c1.company_code=c2.company_code and c1.data_date=c2.data_date
			WHERE c2.data_date = "'''+data_date.strftime("%Y/%m/%d")+'''" and c2.gain_percentage >= '''+str(price_gain_threshold/100)+''' and c1.volume >= '''+str(volume_threshold*1000)+''' 
			order by c1.data_date
			'''
	db_cursor.execute(query)
	result = db_cursor.fetchall()
	print(query)
	return result

def get_by_filter_fshr_gain(data_date, threshold=5, day_num=5):
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	db_cursor = db.cursor(dictionary=True)
	query = '''with DateDifferences AS (
				    SELECT
				        company_code,
				        data_date,
				        foreign_share_holding_ratio,
				        LAG(foreign_share_holding_ratio, '''+str(day_num)+''') OVER (
							PARTITION BY company_code ORDER BY data_date
						) AS foreign_ratio_5_days_before,
				        foreign_share_holding_ratio - LAG(foreign_share_holding_ratio, '''+str(day_num)+''') OVER (PARTITION BY company_code ORDER BY data_date) AS difference
				    FROM
				        company_100_data
				)
				SELECT
				    company_code,
				    data_date,
				    foreign_share_holding_ratio,
				    foreign_ratio_5_days_before,
				    difference
				FROM
				    DateDifferences
				WHERE
					data_date="'''+data_date.strftime("%Y/%m/%d")+'''" and difference > '''+str(threshold)+'''
				ORDER BY
				    company_code, data_date DESC;
			'''
	print(query)
	db_cursor.execute(query)
	result = db_cursor.fetchall()
	# print(query)
	return result

def get_finance_report(company_code):
	db, db_cursor = connect_db(db_name="STOCK_INFO")
	db_cursor = db.cursor(dictionary=True)
	query = '''
				select year,season,EPS FROM finance_report WHERE company_code="{}" ORDER BY year DESC, season DESC LIMIT 4;
			'''
	query = query.format(company_code)
	db_cursor.execute(query)
	result = db_cursor.fetchall()
	# print(query)
	return result

def get_date():
	select_date = Company100Data.objects.order_by('-data_date').values('data_date').distinct()
	select_option=[]
	for i in range(len(select_date)):
		# print(select_date[i])
		tmp=select_date[i]["data_date"].strftime("%Y/%m/%d")
		select_option.append(tmp)
	return select_option