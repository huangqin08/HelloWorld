# Generated by Django 2.0 on 2020-08-07 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_auto_20200807_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True, verbose_name='商品总价'),
        ),
    ]
