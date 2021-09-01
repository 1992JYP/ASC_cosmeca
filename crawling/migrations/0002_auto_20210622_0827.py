# Generated by Django 3.2.4 on 2021-06-21 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawling', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cp_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(db_column='PRODUCT_ID', max_length=50)),
                ('user_name', models.CharField(db_column='USER_NAME', max_length=20)),
                ('grade', models.IntegerField(db_column='GRADE')),
                ('title', models.CharField(db_column='TITLE', max_length=200)),
                ('review', models.TextField(db_column='REVIEW')),
            ],
            options={
                'db_table': 'CP_REVIEW',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Cp_C_Product',
        ),
    ]
