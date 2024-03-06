# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BigPlayerRatio(models.Model):
    company_code = models.CharField(max_length=10)
    data_date = models.DateTimeField(blank=True, null=True)
    ratio = models.FloatField(blank=True, null=True)
    update_time = models.DateTimeField()
    update_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'big_player_ratio'
        unique_together = (('company_code', 'data_date'),)


class CatalogCompany(models.Model):
    company_url = models.CharField(max_length=1000)
    company_code = models.CharField(primary_key=True, max_length=100)
    company_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'catalog_company'


class CatalogCompanyDataDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    average_closing_price = models.FloatField()
    average_volume = models.FloatField()
    company_code = models.ForeignKey(CatalogCompany, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog_company_data_detail'


class CatalogCompanyEverydayData(models.Model):
    id = models.BigAutoField(primary_key=True)
    volume = models.IntegerField()
    closing_price = models.FloatField()
    date = models.DateField()
    company_code = models.ForeignKey(CatalogCompany, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog_company_everyday_data'


class CatalogDropdownlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    dropdownlist_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'catalog_dropdownlist'


class CatalogSelectOption(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.IntegerField()
    text = models.CharField(max_length=100)
    dropdownlist_name = models.ForeignKey(CatalogDropdownlist, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog_select_option'


class Company100Data(models.Model):
    company_code = models.CharField(max_length=10)
    update_time = models.DateTimeField()
    update_name = models.CharField(max_length=20, blank=True, null=True)
    closing_price = models.FloatField(blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    data_date = models.DateTimeField(blank=True, null=True)
    foreign_share_holding_ratio = models.FloatField(blank=True, null=True)
    open_price = models.FloatField(blank=True, null=True)
    high_price = models.FloatField(blank=True, null=True)
    low_price = models.FloatField(blank=True, null=True)
    price_change = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_100_data'
        unique_together = (('company_code', 'data_date'),)


class CompanyHistoryCalculateData(models.Model):
    company_code = models.CharField(max_length=10, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    update_name = models.CharField(max_length=20, blank=True, null=True)
    number_100ma = models.FloatField(db_column='100MA', blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    data_date = models.DateTimeField(blank=True, null=True)
    monthly_avg_volume = models.FloatField(blank=True, null=True)
    gain_percentage = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_history_calculate_data'
        unique_together = (('company_code', 'data_date'),)


class CompanyHistoryData(models.Model):
    company_code = models.CharField(max_length=10)
    update_time = models.DateTimeField()
    update_name = models.CharField(max_length=20, blank=True, null=True)
    closing_price = models.FloatField(blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    data_date = models.DateTimeField(blank=True, null=True)
    foreign_share_holding_ratio = models.FloatField(blank=True, null=True)
    open_price = models.FloatField(blank=True, null=True)
    high_price = models.FloatField(blank=True, null=True)
    low_price = models.CharField(max_length=45, blank=True, null=True)
    price_change = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_history_data'
        unique_together = (('company_code', 'data_date'),)


class CompanyId(models.Model):
    company_name = models.CharField(max_length=20, blank=True, null=True)
    company_type = models.CharField(max_length=5, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    update_name = models.CharField(max_length=20, blank=True, null=True)
    company_code = models.CharField(unique=True, max_length=10, blank=True, null=True)
    capital_amount = models.CharField(max_length=30, blank=True, null=True)
    alive = models.CharField(max_length=10, blank=True, null=True)
    shares_issued = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_id'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class GainOver35(models.Model):
    company_code = models.CharField(max_length=10)
    update_time = models.DateTimeField()
    update_name = models.CharField(max_length=20, blank=True, null=True)
    data_date = models.DateTimeField(blank=True, null=True)
    gain_value = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gain_over_3_5'
        unique_together = (('company_code', 'data_date'),)


class MonthlyAvgVolumeOver2X(models.Model):
    company_code = models.CharField(max_length=10)
    update_time = models.DateTimeField()
    update_name = models.CharField(max_length=20, blank=True, null=True)
    data_date = models.DateTimeField(blank=True, null=True)
    x_times = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monthly_avg_volume_over_2x'
        unique_together = (('company_code', 'data_date'),)


class Over100Ma(models.Model):
    company_code = models.CharField(max_length=10)
    update_time = models.DateTimeField()
    update_name = models.CharField(max_length=20, blank=True, null=True)
    data_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'over_100MA'
        unique_together = (('company_code', 'data_date'),)
