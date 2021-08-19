from django.db import models

# Create your models here.
class BaseModel(models.Model):
    add_time = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    update_time = models.DateTimeField(auto_now_add=True,verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        abstract = True

class GoodsType(BaseModel):
    name = models.CharField(max_length=30, verbose_name='商品类别名称')
    logo = models.CharField(max_length=30, verbose_name='标识')
    image = models.ImageField(upload_to='type', verbose_name='类别图片')

    class Meta:
        db_table = 'goods_type'
        verbose_name = '商品类别表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Goods(BaseModel):
    type = models.ForeignKey('GoodsType', verbose_name='商品种类', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name='商品名称')
    desc = models.CharField(max_length=250, verbose_name='商品简介')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    unite = models.CharField(max_length=20, verbose_name='商品单位')
    image = models.ImageField(upload_to='goods', verbose_name='商品图片')
    stock = models.IntegerField(default=1, verbose_name='商品库存')
    sales = models.IntegerField(default=0, verbose_name='商品销量')
    status = models.SmallIntegerField(default=1, choices=((0, '下线'), (1, '上线')), verbose_name='商品状态')
    detail = models.TextField(verbose_name='商品详情')

    class Meta:
        db_table = 'goods'
        verbose_name = '商品表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class GoodsImage(BaseModel):
    '''商品图片模型类'''
    goods = models.ForeignKey(to=Goods, on_delete=models.CASCADE,verbose_name='商品')
    image = models.ImageField(upload_to='goodsdetail', verbose_name='图片路径')

    class Meta:
        db_table = 'df_goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

# 首页轮播图
class IndexGoodsBanner(BaseModel):
    goods = models.ForeignKey(to=Goods, on_delete=models.CASCADE,verbose_name='商品名称')
    image = models.ImageField(upload_to='banner', verbose_name='商品图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'index_banner'
        verbose_name = '首页轮播图'
        verbose_name_plural = verbose_name

# 主页分类商品展示
class IndexGoodsTypeBanner(BaseModel):
    type = models.ForeignKey(to=GoodsType, verbose_name='商品种类', on_delete=models.CASCADE)
    goods = models.ForeignKey(to=Goods, on_delete=models.CASCADE, verbose_name='广告商品',null=True)
    display_type = models.SmallIntegerField(default=1, choices=((0, '标题'), (1, '图片')),verbose_name='显示类型')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'index_goods_banner'
        verbose_name = '首页分类展示商品表'
        verbose_name_plural = verbose_name

# 主页促销商品
class IndexSaleBanner(BaseModel):
    name = models.CharField(max_length=30, verbose_name='促销活动名称')
    image = models.ImageField(upload_to='sale', verbose_name='活动图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')
    url = models.URLField(verbose_name='活动链接')

    class Meta:
        db_table = 'index_sale'
        verbose_name = '首页促销活动'
        verbose_name_plural = verbose_name
