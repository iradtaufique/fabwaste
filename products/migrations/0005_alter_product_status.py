# Generated by Django 3.2.9 on 2021-12-15 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20211215_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('UnSold', 'UnSold'), ('Collected', 'Collected'), ('Available', 'Available'), ('Denied', 'Denied')], default='Pending', max_length=10),
        ),
    ]
