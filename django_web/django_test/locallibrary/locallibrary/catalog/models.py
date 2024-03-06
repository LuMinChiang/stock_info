from django.db import models
# from locallibrary.models import Company100Data, CompanyHistoryData, CompanyId

# Create your models here.
class company(models.Model):
	company_url = models.URLField(max_length=1000,help_text="該公司連結網址")
	company_code = models.CharField(max_length=100,help_text="股票編號",primary_key=True)
	company_name = models.CharField(max_length=100,help_text="公司名稱")
    
	class Meta:
		ordering = ["company_code"]

	def __str__(self):
		return self.company_code + self.company_name


class company_everyday_data(models.Model):
	company_code = models.ForeignKey("company", on_delete=models.SET_NULL, null=True, help_text="股票編號")
	volume = models.IntegerField(help_text="成交量")
	closing_price = models.FloatField(help_text="收盤價")
	date = models.DateField(help_text="交易日期")

class company_data_detail(models.Model):
	company_code = models.ForeignKey("company", on_delete=models.SET_NULL, null=True)
	average_closing_price = models.FloatField(help_text="平均收盤價")
	average_volume = models.FloatField(help_text="平均成交量")

class dropdownlist(models.Model):
	dropdownlist_name = models.CharField(max_length=100,help_text="下拉選單名稱")

class select_option(models.Model):
	dropdownlist_name = models.ForeignKey("dropdownlist", on_delete=models.SET_NULL, null=True, help_text="下拉選單名稱")
	value = models.IntegerField(help_text="下拉選項編號")
	text = models.CharField(max_length=100, help_text="下拉選項名稱")

class Filter3(models.Model):
    # id = models.CharField(max_length=10,primary_key=True)
    company_code = models.CharField(max_length=10)
    avg_closing_price = models.FloatField(null=True)
    avg_volume = models.FloatField(null=True)
    latest_date = models.DateTimeField(null=True)
    latest_closing_price = models.FloatField(null=True)
    previous_date = models.DateTimeField(null=True)
    previous_closing_price = models.FloatField(null=True)
    closing_price_percentage_diff = models.FloatField(null=True)
    latest_volume = models.FloatField(null=True)
    previous_volume = models.FloatField(null=True)
    volume_percentage_diff = models.FloatField(null=True)
    company_type = models.CharField(max_length=10,null=True)
    max_closing_price = models.FloatField(null=True)
    max_volume = models.FloatField(null=True)
    
    class Meta:
        managed = False
        db_table = 'filter_3'

# class Company100Data(models.Model):
#     company_code = models.CharField(max_length=10)
#     update_time = models.DateTimeField()
#     update_name = models.CharField(max_length=20, blank=True, null=True)
#     closing_price = models.FloatField(blank=True, null=True)
#     volume = models.IntegerField(blank=True, null=True)
#     data_date = models.DateTimeField(blank=True, null=True)
#     foreign_share_holding_ratio = models.FloatField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'company_100_data'


# class CompanyHistoryData(models.Model):
#     company_code = models.CharField(max_length=10)
#     update_time = models.DateTimeField()
#     update_name = models.CharField(max_length=20, blank=True, null=True)
#     closing_price = models.FloatField(blank=True, null=True)
#     volume = models.IntegerField(blank=True, null=True)
#     data_date = models.DateTimeField(blank=True, null=True)
#     foreign_share_holding_ratio = models.FloatField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'company_history_data'
#         unique_together = (('company_code', 'data_date'),)


# class CompanyId(models.Model):
#     company_name = models.CharField(max_length=20, blank=True, null=True)
#     company_type = models.CharField(max_length=5, blank=True, null=True)
#     update_time = models.DateTimeField(blank=True, null=True)
#     update_name = models.CharField(max_length=20, blank=True, null=True)
#     company_code = models.CharField(unique=True, max_length=10, blank=True, null=True)
#     capital_amount = models.CharField(max_length=10, blank=True, null=True)
#     alive = models.CharField(max_length=10, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'company_id'


