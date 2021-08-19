# Generated by Django 2.0 on 2020-08-04 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=20, verbose_name='商品名称')),
                ('desc', models.CharField(max_length=250, verbose_name='商品简介')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品价格')),
                ('unite', models.CharField(max_length=20, verbose_name='商品单位')),
                ('image', models.ImageField(upload_to='goods', verbose_name='商品图片')),
                ('stock', models.IntegerField(default=1, verbose_name='商品库存')),
                ('sales', models.IntegerField(default=0, verbose_name='商品销量')),
                ('status', models.SmallIntegerField(choices=[(0, '下线'), (1, '上线')], default=1, verbose_name='商品状态')),
                ('detail', models.CharField(max_length=800, verbose_name='商品详情')),
            ],
            options={
                'verbose_name': '商品表',
                'verbose_name_plural': '商品表',
                'db_table': 'goods',
            },
        ),
        migrations.CreateModel(
            name='GoodsType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=30, verbose_name='商品类别名称')),
                ('logo', models.CharField(max_length=30, verbose_name='标识')),
                ('image', models.ImageField(upload_to='type', verbose_name='类别图片')),
            ],
            options={
                'verbose_name': '商品类别表',
                'verbose_name_plural': '商品类别表',
                'db_table': 'goods_type',
            },
        ),
        migrations.CreateModel(
            name='IndexGoodsBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('image', models.ImageField(upload_to='banner', verbose_name='商品图片')),
                ('index', models.SmallIntegerField(default=0, verbose_name='展示顺序')),
                ('goods', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='goods.Goods')),
            ],
            options={
                'verbose_name': '首页轮播图',
                'verbose_name_plural': '首页轮播图',
                'db_table': 'index_banner',
            },
        ),
        migrations.CreateModel(
            name='IndexGoodsTypeBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('display_type', models.SmallIntegerField(choices=[(0, '标题'), (1, '图片')], default=1)),
                ('index', models.SmallIntegerField(default=0, verbose_name='展示顺序')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsType', verbose_name='商品种类')),
            ],
            options={
                'verbose_name': '首页分类展示商品表',
                'verbose_name_plural': '首页分类展示商品表',
                'db_table': 'index_goods_banner',
            },
        ),
        migrations.CreateModel(
            name='IndexSaleBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=30, verbose_name='促销活动名称')),
                ('image', models.ImageField(upload_to='sale', verbose_name='活动图片')),
                ('index', models.SmallIntegerField(default=0, verbose_name='展示顺序')),
                ('url', models.URLField(verbose_name='活动链接')),
            ],
            options={
                'verbose_name': '首页促销活动',
                'verbose_name_plural': '首页促销活动',
                'db_table': 'index_sale',
            },
        ),
        migrations.AddField(
            model_name='goods',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsType', verbose_name='商品种类'),
        ),
    ]