# Generated by Django 5.0.1 on 2024-01-10 07:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='company',
            fields=[
                ('company_url', models.URLField(help_text='該公司連結網址', max_length=1000)),
                ('company_code', models.CharField(help_text='股票編號', max_length=100, primary_key=True, serialize=False)),
                ('company_name', models.CharField(help_text='公司名稱', max_length=100)),
            ],
            options={
                'ordering': ['company_code'],
            },
        ),
        migrations.CreateModel(
            name='select_option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('text', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='company_data_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average_closing_price', models.FloatField(help_text='平均收盤價')),
                ('average_volume', models.FloatField(help_text='平均成交量')),
                ('company_code', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.company')),
            ],
        ),
        migrations.CreateModel(
            name='company_everyday_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volume', models.IntegerField(help_text='成交量')),
                ('closing_price', models.FloatField(help_text='收盤價')),
                ('date', models.DateField(help_text='交易日期')),
                ('company_code', models.ForeignKey(help_text='股票編號', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.company')),
            ],
        ),
    ]