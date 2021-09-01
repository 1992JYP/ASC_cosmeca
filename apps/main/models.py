from django.conf.urls import url
from django.db import models
from django.urls.base import reverse_lazy
# Create your models here.
from django.views.generic import CreateView
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm

class Employees(models.Model):
    name = models.CharField(max_length=20)
    position = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'EMPLOYEES'
    
# def queryone(request):
#     print( 1111111)
#     return render(request, loader.get_template('main/dbtest.html'))


class NvProduct(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pd_index = models.IntegerField(db_column='PD_INDEX', blank=True, null=True)  # Field name made lowercase.
    keyword = models.CharField(db_column='KEYWORD', max_length=50, blank=True, null=True)  # Field name made lowercase.
    seller_name = models.CharField(db_column='SELLER_NAME', max_length=20, blank=True, null=True)  # Field name made lowercase.
    reg_date = models.CharField(db_column='REG_DATE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    is_ad = models.CharField(db_column='IS_AD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    price = models.IntegerField(db_column='PRICE', blank=True, null=True)  # Field name made lowercase.
    review_count = models.IntegerField(db_column='REVIEW_COUNT', blank=True, null=True)  # Field name made lowercase.
    serial_number = models.CharField(db_column='SERIAL_NUMBER', max_length=20, blank=True, null=True)  # Field name made lowercase.
    prod = models.CharField(db_column='PROD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    link = models.CharField(db_column='LINK', max_length=500, blank=True, null=True)  # Field name made lowercase.
    score_avg = models.CharField(db_column='SCORE_AVG', max_length=5 , blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(db_column='IMAGE', max_length=500, blank=True, null=True)  # Field name made lowercase.
    date_info = models.DateTimeField(db_column='DATE_INFO', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NV_PRODUCT'


class NvReview(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pd_index = models.IntegerField(db_column='PD_INDEX', blank=True, null=True)  # Field name made lowercase.
    serial_number = models.CharField(db_column='SERIAL_NUMBER', max_length=20, blank=True, null=True)  # Field name made lowercase.
    review_text = models.CharField(db_column='REVIEW_TEXT', max_length=500, blank=True, null=True)  # Field name made lowercase.
    score = models.IntegerField(db_column='SCORE', blank=True, null=True)  # Field name made lowercase.
    p_option = models.CharField(db_column='P_OPTION', max_length=100, blank=True, null=True)  # Field name made lowercase.
    review_date = models.CharField(db_column='REVIEW_DATE', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NV_REVIEW'




