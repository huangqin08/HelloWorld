from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from user.models import User, UserProfile


def register(request):
    user = User()
    user.username = 'xiaoxi'
    user.password = '123456'
    user.phone = '15810888888'
    user.email ='123456@126.com'
    user.save()

    userprofile = UserProfile()
    userprofile.realname = 'lixiaoxi'
    userprofile.address ='北京'
    userprofile.age =22
    userprofile.user_id = user.id
    userprofile.save()
    return HttpResponse('用户注册成功!!!')

def show(request):
    users = User.objects.all()
    return render(request,'user/show.html',context={'users':users})

def delete(request,uid):
    print(uid)
    user = User.objects.get(pk=uid)
    user.delete()
    return HttpResponse('用户删除成功！')

