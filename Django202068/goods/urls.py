from django.urls import path
from goods.views import index,mygoods,my_redirect,mytags,mybootstrap,welcome,register,detail,login,show,delete_user

app_name = 'goods'
urlpatterns = [
    path('',index),
    path('mygoods',mygoods,name='mygoods'),
    path('myreverse',my_redirect,name='myreverse'),
    path('mytags',mytags,name='mytags'),
    path('mybootstrap',mybootstrap,name='mybootstrap'),
    path('welcome',welcome,name='welcome'),
    path('register',register,name='register'),
    path('login',login,name='login'),
    path('show',show,name='show'),
    path('detail',detail,name='detail'),

    path('delete_user',delete_user,name='delete_user'),
]
