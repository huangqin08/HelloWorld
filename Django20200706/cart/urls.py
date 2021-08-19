from django.urls import path
from cart.views import *

app_name ='cart'

urlpatterns =[
    path('add', add_cart,name='add'),
    path('show', show_cart,name='show'),
    path('delete', delete_cart, name='delete'),
]
