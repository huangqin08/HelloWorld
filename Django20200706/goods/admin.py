from django.contrib import admin

# Register your models here.
from goods.models import *

admin.site.register(GoodsType)
admin.site.register(Goods)
admin.site.register(IndexGoodsBanner)
admin.site.register(IndexGoodsTypeBanner)
admin.site.register(IndexSaleBanner)
admin.site.register(GoodsImage)
