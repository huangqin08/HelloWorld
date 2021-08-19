from django.db import models


# Create your models here.
class UserType(models.Model):
    type_name = models.CharField(max_length=50, verbose_name='用户类型')

    class Meta:
        db_table = 'user_type'
        verbose_name = '用户类型表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type_name


class User(models.Model):
    username = models.CharField(max_length=20, verbose_name='用户名', unique=True)
    password = models.CharField(max_length=128, verbose_name='密码')
    phone = models.CharField(max_length=11, verbose_name='手机号码', unique=True)
    email = models.CharField(max_length=50, verbose_name='用户邮箱', null=False)
    address = models.CharField(max_length=30, choices=(('中国', '中国'), ('美国', '美国'), ('俄国', '俄国'), ('法国', '法国')),
                               verbose_name='国家')  # CharField可以用  如果是IntegerField或者SmallIntegerField，choices的第一个就必须写整型值
    is_super = models.BooleanField(default=False, verbose_name='是否是管理员')
    is_active = models.BooleanField(default=False,verbose_name='是否激活用户')
    usertype = models.ForeignKey(to=UserType,on_delete=models.CASCADE)  # to=后面一般放的是类对象，在一个应用中可以用to='',如果不是一个应用，就必须用to=类名

    class Meta:
        db_table = 'user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
