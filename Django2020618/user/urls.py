from django.urls import path
from user.views import *

app_name = 'user'
urlpatterns = [
    path('register',register,name='register'),
    path('login',login,name='login'),
    path('show',show,name='show'),
    path('delete',delete,name='delete'),
    path('update',update,name='update'),
]
