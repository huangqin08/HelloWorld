# Generated by Django 2.0 on 2020-06-19 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterModelTable(
            name='user',
            table='user',
        ),
    ]
