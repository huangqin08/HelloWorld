# Generated by Django 2.0 on 2020-08-03 10:16

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recevier', models.CharField(max_length=20, verbose_name='收件人')),
                ('addr', models.CharField(max_length=250, verbose_name='收件地址')),
                ('zip_code', models.CharField(max_length=6, verbose_name='邮政编码')),
                ('is_default', models.BooleanField(default=False, verbose_name='是否是默认地址')),
                ('phone', models.CharField(max_length=11, verbose_name='收件人联系电话')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '地址表',
                'verbose_name_plural': '地址表',
                'db_table': 'address',
            },
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户表', 'verbose_name_plural': '用户表'},
        ),
        migrations.AlterField(
            model_name='user',
            name='icon',
            field=models.ImageField(upload_to='uploads/%Y/%m/%d/', verbose_name='用户头像'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=11, unique=True, verbose_name='手机号码'),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]