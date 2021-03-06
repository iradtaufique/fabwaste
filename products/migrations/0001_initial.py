# Generated by Django 3.2.9 on 2021-12-20 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('sector', models.CharField(max_length=50)),
                ('cell', models.CharField(max_length=50)),
                ('village', models.CharField(max_length=50)),
                ('road_number', models.CharField(max_length=10)),
                ('house_number', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('minimum_price', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('maximum_price', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('product_image', models.ImageField(upload_to='media')),
                ('description', models.TextField()),
                ('created_date', models.DateField(auto_now_add=True)),
                ('collected_date', models.DateField()),
                ('quantity', models.IntegerField()),
                ('status', models.CharField(choices=[('UnSold', 'UnSold'), ('Collected', 'Collected'), ('Available', 'Available'), ('Denied', 'Denied')], default='Pending', max_length=10)),
                ('payed', models.BooleanField(default=False)),
                ('desired_price', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('buying_price', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('selling_price', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('sector', models.CharField(max_length=100)),
                ('cell', models.CharField(max_length=100)),
                ('village', models.CharField(max_length=100)),
                ('road_number', models.CharField(max_length=100)),
                ('house_number', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.category')),
            ],
        ),
    ]
