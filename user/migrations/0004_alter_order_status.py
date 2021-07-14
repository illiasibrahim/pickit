# Generated by Django 3.2.4 on 2021-07-12 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Dispatched', 'Dispatched'), ('Pending', 'Pending')], default='Pending', max_length=20),
        ),
    ]
