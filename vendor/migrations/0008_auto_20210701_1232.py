# Generated by Django 3.2.4 on 2021-07-01 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0007_category_cat_offer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='product',
            name='discount_price',
        ),
    ]
