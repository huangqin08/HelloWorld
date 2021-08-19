from django.shortcuts import redirect, render
from django.http import HttpResponse

# Create your views here.
from django.urls import reverse

from datetime import datetime

goods = ['苹果','香蕉','火龙果']


def mygoods(request):
    s='便利蜂商品有：<br>'
    for i in goods:
        s += i+ '<br>'
    return HttpResponse(s)

def my_redirect(request):
    url=reverse('goods:mygoods')
    return redirect(url)

class Movie():
    def __init__(self,name,director):
        self.name = name
        self.director = director
    def __str__(self):
        self.name

def index(request):
    # str int
    name = 'admin'
    dtime = datetime.now()
    # float
    score= 7.8
    #list tuple set
    movies = ['我和我的祖国','冰雪奇缘','绿巨人']
    # dict
    stars = {'boy':'蔡徐坤','girl':'虞书欣'}
    # object
    movie = Movie('我和我的祖国','陈凯歌')
    return render(request,'goods.html',context= {'name':name,'dtime':dtime,'score':score,'movies':movies,'stars':stars,'movie':movie})


def mytags(request):
    mag = '<h1>This is a Dog!</h1>'
    movies = ['我和我的祖国', '冰雪奇缘', '绿巨人']
    return render(request,'mytags.html',context={'mag':mag,'movies':movies})

def mybootstrap(request):
    movies = ['我和我的祖国', '冰雪奇缘', '绿巨人','攀登者','少年方世玉','白雪公主','逆风者','烈火英雄']
    page = request.GET.get('page',1)
    # page   start    end
    # 1       0       2
    # 2       2       4
    # 3       4       6
    # 4       6       8
    # 5       8       10
    if int(page) == 1 :
        start = 0
    if int(page) == 2 :
        start = 2
    if int(page) == 3 :
        start = 4
    if int(page) == 4 :
        start = 6
    if int(page) == 5 :
        start = 8
    end = start +2
    movies =movies[start:end]
    return render(request,'mybootstrap.html',context={'movies':movies,'page':int(page)})

#欢迎页面
def welcome(request):
    return render(request, 'welcome.html',context={'num':1000})


# 注册
class User():
    def __init__(self,email,password):
        self.email = email
        self.password = password

    def __str__(self):
        self.email

users = []

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        if password == repassword:
            user= User(email,password)
            users.append(user)
            # return HttpResponse('用户注册成功')
            return redirect(reverse('goods:detail'))
        else:
            return render(request,'register.html',context={'meg':'密码不一致'})

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)
        for user in users:
            if email == user.email and password == user.password:
                # return HttpResponse('登录成功')
                return redirect(reverse('goods:show'))
        else:
            return render(request, 'login.html',context={'mag':'邮箱或密码有误！'})
    return render(request,'login.html')

def show(request):
    return render(request,"show.html",context={'users':users})

def detail(request):
    # email = users[0].email
    return render(request,'detail.html',context={'user':users[0]})

# 删除
def delete_user(request):
    user_id = request.GET.get('user_id')
    print(user_id,type(user_id))
    id = int(user_id) -1
    users.pop(id)
    return HttpResponse("删除成功！")

#更新
