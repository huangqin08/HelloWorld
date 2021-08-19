from django.db import models

# Create your models here.
from goods.models import BaseModel, Goods
from user.models import User, Address


class Order(BaseModel):
    PAY_METHODS=((1,'微信'),(2,'支付宝'),(3,'银联'),(4,'货到付款'))
    ORDER_STATUS=((1,'待付款'),(2,'待发货'),(3,'待收货'),(4,'待评价'),(5,'已完成'))
    order_id = models.CharField(max_length=128,primary_key=True,verbose_name='订单编号')
    user =models.ForeignKey(to=User,on_delete=models.CASCADE,verbose_name='用户')
    address = models.ForeignKey(to=Address,on_delete=models.CASCADE,verbose_name='收货地址')
    pay_method = models.SmallIntegerField(choices=PAY_METHODS,default=2,verbose_name='支付方式')
    goods_number = models.IntegerField(verbose_name='商品总量')
    goods_total = models.DecimalField(max_digits=6,decimal_places=2,verbose_name='商品总价')
    carriage_price = models.IntegerField(default=10,verbose_name='运费')
    order_status = models.SmallIntegerField(choices=ORDER_STATUS,default=1,verbose_name='订单状态')
    trade_no =models.CharField(max_length=128,verbose_name='支付编号')

    class Meta:
        db_table = 'order'
        verbose_name = '订单表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username

class OrderGoods(BaseModel):
    order = models.ForeignKey(to=Order,on_delete=models.CASCADE,verbose_name='订单')
    goods = models.ForeignKey(to=Goods,on_delete=models.CASCADE)
    number = models.IntegerField(default=1,verbose_name='商品数量')
    price = models.DecimalField(max_digits=6,decimal_places=2,verbose_name='商品单价')
    comment = models.CharField(max_length=256,verbose_name='商品评论')

    class Meta:
        db_table = 'ordergoods'
        verbose_name = '订单商品表'
        verbose_name_plural = verbose_name
