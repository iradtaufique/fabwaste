# Generated by Django 3.2.9 on 2021-12-10 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='product_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]