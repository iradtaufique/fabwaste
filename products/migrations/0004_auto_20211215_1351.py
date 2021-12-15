# Generated by Django 3.2.9 on 2021-12-15 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_desired_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='buying_price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='selling_price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='maximum_price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='minimum_price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
    ]
