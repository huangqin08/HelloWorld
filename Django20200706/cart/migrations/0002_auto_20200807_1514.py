# Generated by Django 2.0 on 2020-08-07 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='number',
            field=models.IntegerField(verbose_name='商品数量'),
        ),
    ]