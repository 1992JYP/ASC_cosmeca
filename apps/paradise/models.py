from django.db import models
from django.utils import timezone
from django.db.models import IntegerField, Model
from django.contrib.postgres.fields import ArrayField


class Product(models.Model):
    name = models.CharField(max_length=100,default="test")
    type = models.CharField(max_length=100,default="")
    url = models.CharField(max_length=500,default="")
    body = models.CharField(max_length=10000,default="")
    rank = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    rating = models.FloatField(max_length=6, default=0.0)
    image_file = models.ImageField(max_length=700, upload_to='media', default='default.jpg')
    image_url = models.URLField(max_length=700, default='www.noimage.com')
    # similar_ids=ArrayField(models.IntegerField(), default=list,blank=True)
    
    def __str__(self):
        return self.name

class Review(models.Model):
    name = models.CharField(max_length=100,default="")
    type = models.CharField(max_length=100,default="")
    url = models.CharField(max_length=500,default="")
    body = models.CharField(max_length=10000,default="")
    rank = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    rating = models.FloatField(max_length=6, default=0.0)
    image_file = models.ImageField(max_length=700, upload_to='media', default='default.jpg')
    image_url = models.URLField(max_length=700, default='www.noimage.com')
    # similar_ids=ArrayField(models.IntegerField(), default=list,blank=True)

    def __str__(self):
        return self.name

class Employees(models.Model):
    name = models.CharField(max_length=20)
    position = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'EMPLOYEES'


class CpProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    pd_index = models.IntegerField(db_column='PD_INDEX')  # Field name made lowercase.
    change_index = models.IntegerField(db_column='CHANGE_INDEX')  # Field name made lowercase.
    keyword = models.CharField(db_column='KEYWORD', max_length=50)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=200)  # Field name made lowercase.
    page_link = models.CharField(db_column='PAGE_LINK', max_length=500)  # Field name made lowercase.
    product_id = models.CharField(db_column='PRODUCT_ID', max_length=50)  # Field name made lowercase.
    price = models.IntegerField(db_column='PRICE')  # Field name made lowercase.
    review_count = models.IntegerField(db_column='REVIEW_COUNT')  # Field name made lowercase.
    image_link = models.TextField(db_column='IMAGE_LINK')  # Field name made lowercase.
    item_id = models.CharField(db_column='ITEM_ID', max_length=50)  # Field name made lowercase.
    grade = models.CharField(db_column='GRADE', max_length=5)  # Field name made lowercase.
    date_info = models.DateTimeField(db_column='DATE_INFO')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CP_PRODUCT'


class CpReview(models.Model):
    product_id = models.CharField(db_column='PRODUCT_ID', primary_key=True, max_length=20)  # Field name made lowercase.
    user_name = models.CharField(db_column='USER_NAME', max_length=20)  # Field name made lowercase.
    review_date = models.CharField(db_column='REVIEW_DATE', max_length=10)  # Field name made lowercase.
    score = models.IntegerField(db_column='SCORE')  # Field name made lowercase.
    product_name = models.CharField(db_column='PRODUCT_NAME', max_length=200)  # Field name made lowercase.
    review_text = models.CharField(db_column='REVIEW_TEXT', max_length=500)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CP_REVIEW'
        unique_together = (('product_id', 'user_name', 'review_date', 'review_text'),)



class NvProduct(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pd_index = models.IntegerField(db_column='PD_INDEX', blank=True, null=True)  # Field name made lowercase.
    keyword = models.CharField(db_column='KEYWORD', max_length=50, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    price = models.IntegerField(db_column='PRICE', blank=True, null=True)  # Field name made lowercase.
    review_count = models.IntegerField(db_column='REVIEW_COUNT', blank=True, null=True)  # Field name made lowercase.
    reg_date = models.CharField(db_column='REG_DATE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    seller_name = models.CharField(db_column='SELLER_NAME', max_length=20, blank=True, null=True)  # Field name made lowercase.
    is_ad = models.CharField(db_column='IS_AD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    serial_number = models.CharField(db_column='SERIAL_NUMBER', max_length=20, blank=True, null=True)  # Field name made lowercase.
    prod = models.CharField(db_column='PROD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    link = models.CharField(db_column='LINK', max_length=500, blank=True, null=True)  # Field name made lowercase.
    score_avg = models.DecimalField(db_column='SCORE_AVG', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(db_column='IMAGE', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NV_PRODUCT'


class NvReview(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pd_index = models.IntegerField(db_column='PD_INDEX', blank=True, null=True)  # Field name made lowercase.
    serial_number = models.CharField(db_column='SERIAL_NUMBER', max_length=20, blank=True, null=True)  # Field name made lowercase.
    review_text = models.CharField(db_column='REVIEW_TEXT', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    score = models.IntegerField(db_column='SCORE', blank=True, null=True)  # Field name made lowercase.
    p_option = models.CharField(db_column='P_OPTION', max_length=100, blank=True, null=True)  # Field name made lowercase.
    review_date = models.CharField(db_column='REVIEW_DATE', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NV_REVIEW'


class ProductMaster(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pd_manager = models.CharField(db_column='PD_MANAGER', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pd_code = models.CharField(db_column='PD_CODE', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pd_name = models.CharField(db_column='PD_NAME', max_length=45, blank=True, null=True)  # Field name made lowercase.
    pd_brand = models.CharField(db_column='PD_BRAND', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pd_keyword = models.CharField(db_column='PD_KEYWORD', max_length=12, blank=True, null=True)  # Field name made lowercase.
    nv_code = models.CharField(db_column='NV_CODE', max_length=45, blank=True, null=True)  # Field name made lowercase.
    nv_url = models.CharField(db_column='NV_URL', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    cp_url = models.CharField(db_column='CP_URL', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(db_column='IMAGE', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'PRODUCT_MASTER'