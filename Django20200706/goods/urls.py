from django.urls import path

from goods.views import index,goods_detail

app_name ='goods'

urlpatterns =[
    path('', index,name='index'),
    path('detail/<int:gid>', goods_detail, name='detail'),
]
