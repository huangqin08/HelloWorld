import hashlib

from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse

# Create your views here.
from user.models import User

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        phone = request.POST.get('phone')
        if username and password and repassword:
            if password == repassword:
                # 数据库添加
                # 方式一：
                # user = User()
                # user.username = username
                # user.password = hashlib.sha256(password.encode('utf-8')).hexdigest()   #密码加密
                # if phone:
                #     user.phone = phone
                # user.save()

                # 方式二：
                password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                user = User.objects.create(username=username,password=password,phone=phone)
                if user:
                    return HttpResponse('用户注册成功！')
            else:
                return render(request,'user/register.html',context={'meg':'确认密码不一致！'})
        else:
            return render(request, 'user/register.html', context={'meg': '用户名、密码和确认密码不能为空！'})
    return render(request,'user/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = User.objects.filter(username=username).first()
            password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if user:
                if user.password == password:
                    # return HttpResponse('用户登录成功！')
                    return redirect(reverse('user:show'))
            return render(request, 'user/login.html', context={'meg': '用户名或密码有误！'})
        else:
            return render(request, 'user/login.html',context={'meg':'用户名和密码不能为空！'})
    return render(request,'user/login.html')

def show(request):
    # users = User.objects.all()   # 物理删除
    users = User.objects.filter(is_delete=0).all()
    # print(users)
    return render(request,'user/show.html',context={'users':users})

def delete(request):
    id = request.GET.get('id')
    #根据id去数据库中执行查询
    user = User.objects.get(pk=id)
    if user:
        #删除  物理删除
        # result = user.delete()
        # print(result)
        user.is_delete = 1
        user.save()
        return redirect(reverse('user:show'))
    else:
        return HttpResponse('删除失败！')

def update(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        is_delete = request.POST.get('is_delete')
        print(is_delete)
        #更新的是哪个用户？
        # 方式1
        # user = User.objects.get(pk=id)
        # print(user)
        # user.username = username
        # user.phone = phone
        # user.is_delete = bool(is_delete)
        # user.save()
        # 方式2
        # result = User.objects.filter(id=id).update(username=username,phone=phone,is_delete=bool(is_delete))
        # print(result)
        # return redirect(reverse('user:show'))

        # ajax方式

        result = User.objects.filter(id=id).update(username=username, phone=phone, is_delete=is_delete)
        if result ==1 :
            return JsonResponse({'msg':'success'})
        else:
            return JsonResponse({'msg':'fail'})
    else:
        id = request.GET.get('id')
        # print(id)
        user = User.objects.get(pk=id)
        if user:
            return render(request,'user/update.html',context={'user':user})
        else:
            return redirect(reverse('user:show'))
