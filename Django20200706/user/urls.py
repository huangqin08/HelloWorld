from django.urls import path

from user.views import *

app_name ='user'

urlpatterns =[
    path('index', index,name='index'),
    path('register', register, name='register'),
    path('check_user', check_user,name='check_user'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('active', user_active, name='active'),
    path('forget_pwd', forget_pwd, name='forget_pwd'),
    path('send_code', send_code, name='send_code'),
    path('modify_pwd', modify_pwd, name='modify_pwd'),
    path('center', user_center, name='center'),
    path('modify_icon', modify_icon, name='modify_icon'),
    path('address', address, name='address'),
    path('order', user_order, name='order'),
]
