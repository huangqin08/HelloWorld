from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# class UserManager(models.Manager):
#     #重写
#     def get_queryset(self):
#         return super(UserManager,self).get_queryset().filter(is_delete=0)
#
# class User1(models.Model):
#     username = models.CharField(max_length=150,unique=True)
#     password = models.CharField(max_length=20)
#     is_delete = models.BooleanField(default=False)
#
#     objects = UserManager()
#
#     def __str__(self):
#         return self.username
#
#     class Meta:
#         db_table = 'user'

class User(AbstractUser):
    phone = models.CharField(max_length=11,unique=True,verbose_name='手机号码')
    icon = models.ImageField(upload_to='uploads/%Y/%m/%d/',verbose_name='用户头像')

    class Meta:
        db_table = 'user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

class Address(models.Model):
    recevier = models.CharField(max_length=20,verbose_name='收件人')
    addr = models.CharField(max_length=250,verbose_name='收件地址')
    zip_code = models.CharField(max_length=6,verbose_name='邮政编码')
    is_default= models.BooleanField(default=False,verbose_name='是否是默认地址')
    phone = models.CharField(max_length=11,verbose_name='收件人联系电话')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')
    user = models.ForeignKey(to=User,on_delete=models.CASCADE,verbose_name='所属用户')

    class Meta:
        db_table = 'address'
        verbose_name = '地址表'
        verbose_name_plural = verbose_name
