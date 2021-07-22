
# Generated by Django 3.2.4 on 2021-07-14 16:26


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_title', models.CharField(max_length=50)),
                ('banner', models.ImageField(upload_to='photos/banner')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=50, unique=True)),
                ('time_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, unique=True)),
                ('cat_image', models.ImageField(upload_to='photos/categories')),
                ('cat_offer', models.IntegerField(default=0)),
                ('time_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poster_name', models.CharField(max_length=40)),
                ('poster', models.ImageField(upload_to='photos/poster')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, unique=True)),
                ('mrp', models.IntegerField()),
                ('offer', models.IntegerField(default=0)),
                ('quantity', models.CharField(max_length=10)),
                ('description', models.TextField(blank=True)),
                ('image_1', models.ImageField(upload_to='photos/products/primary')),
                ('image_2', models.ImageField(upload_to='photos/products/secondary')),
                ('image_3', models.ImageField(blank=True, upload_to='photos/products/secondary')),
                ('image_4', models.ImageField(blank=True, upload_to='photos/products/secondary')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.category')),
            ],
        ),
    ]
