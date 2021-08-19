from django.urls import path
from user.views import register, show,delete

app_name = 'user'
urlpatterns = [
    path('register',register,name='register'),
    path('show',show,name='show'),
    path('delete/<int:uid>',delete,name='delete'),
]
