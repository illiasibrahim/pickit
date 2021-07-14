# Generated by Django 3.2.4 on 2021-07-12 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Dispatched', 'Dispatched'), ('Accepted', 'Accepted'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
    ]
