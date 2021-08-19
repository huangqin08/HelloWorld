from django.shortcuts import render

# Create your views here.
from user.forms import UserLoginForm


def user_login(request):
    user_login_1 = UserLoginForm(request.POST)
    return render(request,'user/login.html',locals())
