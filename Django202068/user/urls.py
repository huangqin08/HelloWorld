from django.urls import path
from user.views import index,article,show_article

app_name = 'user'
urlpatterns = [
    path('',index),
    path('article/<int:num>',article,name='article'),
    path('article/<str:name>',show_article,name='article'),
]
