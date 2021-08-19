import hashlib
import time
import uuid

import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from Django20200706 import settings
from Django20200706.settings import MEDIA_URL
from order.models import Order
from user.models import User, Address


# 这是一个测试接口
def test_api(request):
    if request.method == 'POST':
        print('这个是一个POST请求---->')
        phone = request.POST.get('phone')  # 获取前端页面ajax发送过来的数据

        request_data = {  # 这是经过服务器处理之后需要返回给前端的数据
            'phone': phone
        }
    return JsonResponse(request_data)


# 登录后的首页
def index(request):
    # # 获取session
    # username = request.session.get('username')
    # user = User.objects.filter(username=username).first()
    return render(request, 'user/index.html')


# 用户注册
def register(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        email = request.POST.get('E-mail')
        phone = request.POST.get('Phone')
        password = make_password(password)
        user = User.objects.create(username=username, password=password, email=email, phone=phone)
        user.is_active = 0
        user.save()

        # 生成token
        token = str(uuid.uuid4()).replace('-', '')
        # request.session获取一个session对象   当成一个字典
        request.session[token] = user.id

        path = 'http://127.0.0.1:8000/user/active?token={}'.format(token)  # 信息格式化

        # 发送邮箱激活
        subject = '未来鲜生激活邮件'
        message = '''
        欢迎注册未来鲜生会员！亲爱的用户请赶快激活使用吧！
        <br>
        <a href='{}'>点击激活</a>   
        <br>如果链接不可用可以复制以下内容到浏览器激活：
        <br>
        {}
        <br>                            未来鲜生开发团队   
        '''.format(path, path)  # 信息格式化
        result = send_mail(subject=subject, message='', from_email=settings.EMAIL_HOST_USER, recipient_list=[email, ],
                           html_message=message)

        return HttpResponse('注册成功')
    return render(request, 'user/register.html')


# 验证用户是否已注册
def check_user(request):
    username = request.GET.get('username')
    user = User.objects.filter(username=username).first()
    if user:
        return JsonResponse({'status': 'fail', 'msg': '用户名已被占用！'})
    else:
        return JsonResponse({'status': 'success', 'msg': '用户名可用！'})


# 用户邮箱激活
def user_active(request):
    token = request.GET.get('token')
    # 获取session中值
    uid = request.session.get(token)

    user = User.objects.get(pk=uid)
    user.is_active = 1
    user.save()
    return redirect(reverse('user:login'))


# 用户登录
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('userName')
        password = request.POST.get('password')
        rem_name = request.POST.get('rem_name')
        # print('rem_name',rem_name)

        # 使用authenticate()方法做用户登录
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)  # 自动做session
            response = redirect(reverse('user:index'))
            if rem_name == 'on':
                response.set_cookie('uname', username)
            return response
        else:
            return render(request, 'user/login.html', {'msg': '用户名和密码不正确！'})

    #     user = User.objects.filter(username=username).first()
    #     if user:
    #         if user.is_active:
    #             if check_password(password,user.password):
    #                 respones = redirect(reverse('user:index'))
    #                 # 登录成功后，保存当前用户的session
    #                 request.session['username'] =user.username
    #                 if rem_name == 'on':
    #                 # 登录成功后，在cookie中设置值
    #                 # request.COOKIES['uname']=user.username  #错误写法
    #                     respones.set_cookie('uname',username)
    #                 return response
    #             else:
    #                 return render(request, 'user/login.html', {'msg': '用户名和密码不正确！'})
    #         else:
    #             return render(request, 'user/login.html', {'msg': '用户名还未激活！'})
    #     else:
    #         return render(request, 'user/login.html',{'msg':'用户名和密码不正确！'})

    else:
        username = request.COOKIES.get('uname', '')
        return render(request, 'user/login.html', {'username': username})


# 注销，清空session
def user_logout(request):
    # request.session.flush()
    logout(request)
    return redirect(reverse("user:index"))


# 忘记密码
def forget_pwd(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        code = request.POST.get('code')
        if request.session.get(phone) == code:
            return render(request, 'user/modify_pwd.html', {'phone': phone})
        else:
            return render(request, 'user/forget_pwd.html', {'msg': '验证码不正确！'})
    return render(request, 'user/forget_pwd.html')


# 发送验证码
def send_code(request):
    phone = request.GET.get('phone')
    # 寻求第三方服务：网易云信
    url = 'https://api.netease.im/sms/sendcode.action'
    headers = {}
    headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
    headers['AppKey'] = 'c319e6d69853d2834d970fdd0d9b84b9'
    AppSecret = '03d4b504974c'
    Nonce = str(uuid.uuid4()).replace('-', '')
    headers['Nonce'] = Nonce
    CurTime = str(int(time.time()))
    headers['CurTime'] = CurTime
    CheckSum = hashlib.sha1((AppSecret + Nonce + CurTime).encode('utf-8')).hexdigest()
    headers['CheckSum'] = CheckSum
    response = requests.post(url=url, data={'mobile': phone}, headers=headers)
    json_result = response.json()
    if json_result.get('code') == 200:
        request.session[phone] = json_result.get('obj')
        return JsonResponse({'msg': '短信发送成功！'})
    else:
        return JsonResponse({'msg': '短信发送失败！'})


# 用手机号码找到用户后修改密码
def modify_pwd(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        new_password = request.POST.get('password')
        user = User.objects.filter(phone=phone).first()
        password = make_password(new_password)
        user.password = password
        user.save()
        return redirect(reverse('user:login'))
    return render(request, 'user/modify_pwd.html')


# 用户中心
def user_center(request):
    # username = request.session.get('username')
    # user = User.objects.filter(username=username).first()
    msg = '<b>好甜好甜</b>的大苹果！好甜好甜的大苹果！好甜好甜的大苹果！好甜好甜的大苹果！好甜好甜的大苹果！好甜好甜的大苹果！<font color="red">好甜好甜</font>的大苹果！好甜好甜的大苹果！好甜好甜的大苹果！'
    msg.isspace()
    return render(request, 'user/center.html', {'msg': msg})


# 修改图片
def modify_icon(request):
    print('-' * 5, 'jinlai')
    uid = request.POST.get('uid')
    icon = request.FILES.get('icon')
    print('uid', uid)
    user = User.objects.get(pk=uid)
    print(user)
    user.icon = icon
    user.save()
    return JsonResponse({'msg': 'ok', 'image': str(user.icon)})


# 收货地址
def address(request):
    if request.method == 'POST':
        recevier = request.POST.get('recevier')
        addr = request.POST.get('addr')
        phone = request.POST.get('phone')
        zipcode = request.POST.get('zip_code')
        addr = Address.objects.create(recevier=recevier, addr=addr, phone=phone, zip_code=zipcode, user=request.user)
        if addr:
            return redirect(reverse('user:address'))
        else:
            return render(request, 'user/center.html', {"errmsg": '地址添加失败！'})
    else:
        addr = Address.objects.filter(is_default=True).first()
        return render(request, 'user/address.html', {"address": addr})


def user_order(request):
    '''全部订单'''
    orders = Order.objects.filter(user=request.user).order_by('add_time')
    order_list = []
    ordergoods_list = []
    for order in orders:
        for status in Order.ORDER_STATUS:
            if order.order_status in status:
                order.status = status[1]
                break
        order_list.append({'add_time': order.add_time, 'order_id': order.order_id, 'status': order.status,
                           'total': order.goods_total})

        for ordergoods in order.ordergoods_set.all():
            ordergoods_list.append({'order_id': ordergoods.order.order_id,
                                    'image': MEDIA_URL + str(ordergoods.goods.image),
                                    'name': ordergoods.goods.name,
                                    'price': ordergoods.goods.price,
                                    'unite': ordergoods.goods.unite,
                                    'number': ordergoods.number,
                                    'orderprice': ordergoods.price})
    # 订单分页
    paginator = Paginator(orders, 2)  # 每一页的订单数
    page = request.GET.get('page', '1')  # 获取页码值，page对象
    try:
        page = int(page)
    except Exception as err:
        page = 1
    page_obj = str(paginator.page(page))  #报Object of type 'Page' is not JSON serializable 错，解决办法：加上str()

    response_data = [{'order_list': order_list,
                      'ordergoods_list': ordergoods_list,
                     'page_obj':page_obj}]
    return JsonResponse(response_data, safe=False)
