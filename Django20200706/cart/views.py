from django.http import JsonResponse

# Create your views here.
from Django20200706.settings import MEDIA_URL
from cart.models import Cart
from goods.models import Goods

def add_cart(request):
    '''
    加入购物车
    goodsId:商品ID
    number：商品数量
    total：商品总价
    '''
    gid =  request.GET.get('goodsId')
    number = request.GET.get('number')
    total = request.GET.get('total')
    flag = False
    if Cart.objects.filter(goods_id=gid,user=request.user).count()>0:
        cart = Cart.objects.get(goods_id=gid, user=request.user)
        cart.number += int(number)

        total1=float(cart.total)
        total=float(total)+total1
        cart.total=total

        cart.save()
        flag = True
    else:
        goods = Goods.objects.get(pk=gid)
        cart = Cart.objects.create(goods=goods,user=request.user,number=number,total=total)
        if cart:
            flag = True

    if flag:
        count = Cart.objects.filter(user=request.user).count()
        return JsonResponse({'status':'200','count':count})
    else:
        return JsonResponse({'status':'401'})

def show_cart(request):
    '''展示购物车'''
    carts = Cart.objects.filter(user=request.user).all()
    cart_list = []
    for cart in carts:
        cart_list.append({'id':cart.goods.id,
                          'name':cart.goods.name,
                          'image':MEDIA_URL+str(cart.goods.image),
                          'price':cart.goods.price,
                          'unite':cart.goods.unite,
                          'number':cart.number,
                          'total':cart.total})
    count = carts.count()
    response_data = {'cart_list':cart_list,
                     'count': count}
    return JsonResponse(response_data)

def delete_cart(request):
    '''
    删除购物车
    gid：商品ID
    '''
    gid = request.GET.get('gid')
    result = Cart.objects.filter(user=request.user,goods_id=gid).delete()
    print(result)
    if result[0]==1:
        return JsonResponse({'status':'200'})
    else:
        return JsonResponse({'msg': '购物车中无此商品！'})
