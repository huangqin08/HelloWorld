from datetime import datetime

from django.db import models

# Create your models here.
from user.models import User


class Type(models.Model):
    tname = models.CharField(max_length=200,null=False,blank=False)
    add_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.tname

    class Meta:
        db_table = 'type'

class Goods(models.Model):
    gname = models.CharField(max_length=200,null=False,blank=False)
    price = models.DecimalField(max_digits=6,decimal_places=2,null=False)
    sale_num = models.IntegerField(default=0)
    store_num = models.IntegerField(default=0)
    save_num =models.IntegerField(default=0)
    type = models.ForeignKey(to=Type,on_delete=models.CASCADE)

    users = models.ManyToManyField(to=User)

    def __str__(self):
        return self.gname

    class Meta:
        db_table = 'goods'

class Order(models.Model):
    user_id = models.ForeignKey(to=User,on_delete=models.CASCADE)
    goods_id = models.ForeignKey(to=User,on_delete=models.CASCADE)
    number = models.IntegerField(default=1)

    class Meta:
        db_table = 'order'
