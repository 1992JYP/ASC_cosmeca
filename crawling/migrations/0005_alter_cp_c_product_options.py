# Generated by Django 3.2.4 on 2021-06-22 23:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawling', '0004_auto_20210622_0835'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cp_c_product',
            options={'managed': False, 'ordering': ['-grade']},
        ),
    ]
