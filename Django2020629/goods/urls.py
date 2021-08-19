from django.urls import path

from goods.views import add,show_type,goods_show,goods_detail,save_goods,type_delete,add_cart,show_cart,remove_cart

app_name ='goods'

urlpatterns = [
    path('add', add,name='add'),
    path('show_type', show_type,name='show_type'),
    path('goods_show/<int:tid>', goods_show,name='goods_show'),
    path('goods_detail/<int:gid>', goods_detail, name='goods_detail'),
    path('save_goods', save_goods, name='save_goods'),
    path('type_delete/<int:tid>', type_delete, name='type_delete'),
    path('add_cart', add_cart, name='add_cart'),
    path('show_cart', show_cart, name='show_cart'),
    path('remove_cart', remove_cart, name='remove_cart'),
]
