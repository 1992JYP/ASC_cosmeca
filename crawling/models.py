## 작성 2021-06-17  - 이유인 
## 수정  2021- 07-09  - 이유인

from django.db import models

# Create your models here.
# index_num,item_name, link,pid, price,review_count,image_path,vendor_itemId


# 여기가 models.py에서 설계한 모델을 가져오는 코드입니다






    
    # is_public = models.BooleanField(default=False, verbose_name='공개여부')    공개 여부 
    # photo = models.ImageField(blank=True, upload_to=Crawling/item/%Y%m%d')    사진파일 저장
    #java의 tostring
    # def __str__(self):
    #     # return f'Custom Crawling_item object ({self.item_name})




# 자동 입력 옵션  index/date   
# alter table CP_PRODUCT add DATE_INFO TIMESTAMP DEFAULT NOW(); 

class Cp_c_Product(models.Model):
    pd_index = models.IntegerField(db_column='PD_INDEX')  # Field name made lowercase.
    change_index = models.IntegerField(db_column='CHANGE_INDEX')  # Field name made lowercase. 
    company = models.IntegerField(db_column='COMPANY')  # Field name made lowercase.
    keyword = models.CharField(db_column='KEYWORD', max_length=50)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=200)  # Field name made lowercase.
    state = models.IntegerField(db_column='STATE')  # Field name made lowercase.
    page_link = models.CharField(db_column='PAGE_LINK', max_length=500)  # Field name made lowercase.
    product_id = models.CharField(db_column='PRODUCT_ID', max_length=50)  # Field name made lowercase.
    price = models.IntegerField(db_column='PRICE')  # Field name made lowercase.
    review_count = models.IntegerField(db_column='REVIEW_COUNT')  # Field name made lowercase.
    image_link = models.TextField(db_column='IMAGE_LINK')  # Field name made lowercase.
    item_id = models.CharField(db_column='ITEM_ID', max_length=50)  # Field name made lowercase.
    grade = models.CharField(db_column='GRADE', max_length=5)  # Field name made lowercase.
    date_info = models.DateTimeField(db_column='DATE_INFO')  # Field name made lowercase.
    
    class Meta:
        ordering = ['-grade']   # 기본 정렬 설정 하기  -가 붙으면 역순
        managed = False
        db_table = 'CP_PRODUCT'


class Cp_review(models.Model):
    product_id = models.CharField(db_column='PRODUCT_ID', max_length=50)  # Field name made lowercase.
    user_name = models.CharField(db_column='USER_NAME', max_length=50)  # Field name made lowercase.
    date = models.CharField(db_column='DATE', max_length=20)  # Field name made lowercase.
    grade = models.IntegerField(db_column='GRADE')  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=200)  # Field name made lowercase.
    review = models.TextField(db_column='REVIEW')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'CP_REVIEW'


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
    date_info = models.DateTimeField(db_column='DATE_INFO', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NV_PRODUCT'


class NvReview(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pd_index = models.IntegerField(db_column='PD_INDEX', blank=True, null=True)  # Field name made lowercase.
    serial_number = models.CharField(db_column='SERIAL_NUMBER', max_length=20, blank=True, null=True)  # Field name made lowercase.
    review_text = models.TextField(db_column='REVIEW_TEXT', blank=True, null=True)  # Field name made lowercase.
    score = models.IntegerField(db_column='SCORE', blank=True, null=True)  # Field name made lowercase.
    p_option = models.CharField(db_column='P_OPTION', max_length=100, blank=True, null=True)  # Field name made lowercase.
    review_date = models.CharField(db_column='REVIEW_DATE', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NV_REVIEW'