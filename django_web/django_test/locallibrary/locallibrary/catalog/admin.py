from django.contrib import admin
from .models import *
# from locallibrary.models import Company100Data, CompanyHistoryData, CompanyId

# Register your models here.
admin.site.register(company)
admin.site.register(company_everyday_data)
admin.site.register(company_data_detail)
admin.site.register(dropdownlist)
admin.site.register(select_option)
# admin.site.register(Company100Data)
# admin.site.register(CompanyHistoryData)
# admin.site.register(CompanyId)