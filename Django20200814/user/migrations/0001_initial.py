# Generated by Django 2.0 on 2020-08-18 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=128, verbose_name='密码')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='手机号码')),
                ('email', models.CharField(max_length=50, verbose_name='用户邮箱')),
                ('address', models.CharField(choices=[('中国', '中国'), ('美国', '美国'), ('俄国', '俄国'), ('法国', '法国')], max_length=30, verbose_name='国家')),
                ('is_super', models.BooleanField(default=False, verbose_name='是否是管理员')),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=50, verbose_name='用户类型')),
            ],
            options={
                'verbose_name': '用户类型表',
                'verbose_name_plural': '用户类型表',
                'db_table': 'user_type',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='usertype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserType'),
        ),
    ]
