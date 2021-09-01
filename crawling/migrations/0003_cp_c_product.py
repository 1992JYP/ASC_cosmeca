# Generated by Django 3.2.4 on 2021-06-21 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawling', '0002_auto_20210622_0827'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cp_c_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pd_index', models.IntegerField(db_column='PD_INDEX')),
                ('keyword', models.CharField(db_column='KEYWORD', max_length=50)),
                ('title', models.CharField(db_column='TITLE', max_length=200)),
                ('page_link', models.CharField(db_column='PAGE_LINK', max_length=500)),
                ('product_id', models.CharField(db_column='PRODUCT_ID', max_length=50)),
                ('price', models.IntegerField(db_column='PRICE')),
                ('review_count', models.IntegerField(db_column='REVIEW_COUNT')),
                ('image_link', models.TextField(db_column='IMAGE_LINK')),
                ('item_id', models.CharField(db_column='ITEM_ID', max_length=50)),
            ],
            options={
                'db_table': 'CP_PRODUCT',
                'managed': False,
            },
        ),
    ]