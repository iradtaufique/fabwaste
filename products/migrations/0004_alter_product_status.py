# Generated by Django 3.2.9 on 2021-12-21 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20211221_0554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('Collected', 'Collected'), ('Pending', 'Pending'), ('Denied', 'Denied')], default='Pending', max_length=10),
        ),
    ]
