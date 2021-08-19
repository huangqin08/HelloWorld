from datetime import datetime

from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=12,unique=True,null=False,blank=False)  #null=False  表示不能为空，blank=False 表示表单上不能是空字符串
    password = models.CharField(max_length=100,null=False,blank=False)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=50)
    add_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'

#补充表
class UserProfile(models.Model):
    realname = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    age = models.IntegerField()
    job = models.CharField(max_length=50)
    gender = models.CharField(max_length=5,choices=(('boy','男'),('girl','女')))
    user = models.OneToOneField(to=User,on_delete=models.CASCADE)   # CASCADE 表示级联删除，主表删除子表的数据就删除    PROTECT 表示子表数据受保护

    class Meta:
        db_table = 'userprofile'
