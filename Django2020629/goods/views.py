from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from goods.models import Type, Goods
from user.models import User

#商品添加
def add(request):
    if request.method == 'POST':
        gname = request.POST.get('gname')
        price = request.POST.get('price')
        type = request.POST.get('type')
        goods = Goods.objects.create(gname=gname,price=price,type_id=type)
        if goods:
            return HttpResponse('商品添加成功！')
    else:
        types = Type.objects.all()
        return render(request,'goods/add.html',context={'types':types})

#商品分类展示
def show_type(request):
    types = Type.objects.all()
    return render(request,'goods/show_type.html',context={'types':types})

#该分类下的商品展示页
def goods_show(request,tid):
    print('------',tid)
    type = Type.objects.get(pk=tid)
    return render(request, 'goods/goods_show.html',context={'type':type})

#商品详情页
def goods_detail(request,gid):
    goods = Goods.objects.get(pk=gid)
    return render(request,'goods/goods_detail.html',context={'goods':goods})

# 收藏商品
def save_goods(request):
    #明确收藏的是哪个商品？ id
    id =request.GET.get('id')
    flag =request.GET.get('flag')
    #查询数据库找商品根据id
    goods = Goods.objects.get(pk=id)
    #商品对象.save_num +=1
    if goods:
        if flag=='unsave':
            goods.save_num += 1
        elif flag=='save':
            goods.save_num -= 1
        goods.save()   #更新后需要保存一下
        # 返回结果
        return JsonResponse({'msg':'success','number':goods.save_num})  #需要把更新后的数据返回回去
    else:
        return JsonResponse({'msg': 'fail'})

# 删除商品分类
def type_delete(request,tid):
    type = Type.objects.get(pk=tid)
    type.delete()
    return HttpResponse('商品分类删除成功！')

#加入购物车
def add_cart(request):
    id = request.GET.get('id')
    user = User.objects.get(pk=3)
    goods = Goods.objects.get(pk=id)
    user.goods_set.add(goods)
    # goods.users.add(user)
    return JsonResponse({'msg': 'success'})

#查看购物车
def show_cart(request):
    user = User.objects.get(pk=3)
    goods = user.goods_set.all()
    return render(request, 'goods/show_cart.html', context={'goods': goods,'user':user})

#移除购物车
def remove_cart(request):
    id = request.GET.get('id')
    user = User.objects.get(pk=3)
    goods = Goods.objects.get(pk=id)
    user.goods_set.remove(goods)
    return redirect(reverse('goods:show_cart'))
    # return HttpResponse('商品分类删除成功！')
