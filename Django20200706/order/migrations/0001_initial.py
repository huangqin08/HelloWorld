# Generated by Django 2.0 on 2020-08-10 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0003_auto_20200804_0923'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goods', '0005_auto_20200806_1600'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('order_id', models.CharField(max_length=128, primary_key=True, serialize=False, verbose_name='订单编号')),
                ('pay_method', models.SmallIntegerField(choices=[(1, '微信'), (2, '支付宝'), (3, '银联'), (4, '货到付款')], default=2, verbose_name='支付方式')),
                ('goods_number', models.IntegerField(verbose_name='商品总量')),
                ('goods_total', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='商品总价')),
                ('carriage_price', models.IntegerField(default=10, verbose_name='运费')),
                ('order_status', models.SmallIntegerField(choices=[(1, '待付款'), (2, '待发货'), (3, '待收货'), (4, '待评价'), (5, '已完成')], default=1, verbose_name='订单状态')),
                ('trade_no', models.CharField(max_length=128, verbose_name='支付编号')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Address', verbose_name='收货地址')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '订单表',
                'verbose_name_plural': '订单表',
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('number', models.IntegerField(default=1, verbose_name='商品数量')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='商品单价')),
                ('comment', models.CharField(max_length=256, verbose_name='商品评论')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order', verbose_name='订单')),
            ],
            options={
                'verbose_name': '订单商品表',
                'verbose_name_plural': '订单商品表',
                'db_table': 'ordergoods',
            },
        ),
    ]
