from django.db import models

# Create your models here.
from goods.models import BaseModel, Goods
from user.models import User


class Cart(BaseModel):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    goods = models.ForeignKey(to=Goods,on_delete=models.CASCADE)
    number = models.IntegerField(verbose_name='商品数量')
    total = models.DecimalField(max_digits=6,decimal_places=2,verbose_name='商品总价',null=True)
    class Meta:
        db_table = 'cart'
        verbose_name = '购物车表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
