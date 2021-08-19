from datetime import datetime

from alipay import AliPay
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
import order
from Django20200706 import settings
from Django20200706.settings import MEDIA_URL
from cart.models import Cart
from goods.models import Goods
from order.models import Order, OrderGoods
from user.models import Address


def generate_order(request):
    '''去结算订单
    goods_1：购物车中需要结算的商品ID
    '''
    gid_list = request.POST.getlist('goods_1')
    if not gid_list:
        return JsonResponse({'msg': '没有勾选任何商品！'})
    order_goods_list = []
    goods_order_number = 0
    goods_order_total = 0
    # 遍历 商品id列表
    for gid in gid_list:
        # 商品对象
        goods = Goods.objects.get(pk=gid)
        # 去购物车获取该商品的信息
        cart_goods = Cart.objects.get(goods=goods, user=request.user)
        # 动态设置商品的属性 获取购物车信息并将信息设置给商品对象
        goods.number = cart_goods.number  # 当前下订单的商品数量
        goods.total = cart_goods.total  # 当前下订单的商品总价
        ##添加到商品列表中
        order_goods_list.append({'image': MEDIA_URL + str(goods.image),
                                 'name': goods.name,
                                 'unite': goods.unite,
                                 'price': goods.price,
                                 'number': goods.number,
                                 'total': goods.total})
        # 该订单的所有商品的总数量和总价格
        goods_order_number += cart_goods.number
        goods_order_total += cart_goods.total
        print(type(goods_order_total))
        print(type(cart_goods.total))
    # 一共多少件商品
    num = len(order_goods_list)
    print(num)
    # 写死运费
    carriage_price = 10
    # 真实付款价格
    real_pay_total = goods_order_total + carriage_price
    # 收货地址
    addrs = Address.objects.filter(user=request.user)
    addr_list = []
    for addr1 in addrs:
        addr_list.append({'add': addr1.addr, 'recevier': addr1.recevier, 'phone': addr1.phone})
    # 辅助作用的字段
    gid_list_str = ','.join(gid_list)
    response_data = [{'order_goods_list': order_goods_list,
                      'goods_order_number': goods_order_number,
                      'goods_order_total': goods_order_total,
                      'carriage_price': carriage_price,
                      'real_pay_total': real_pay_total,
                      'add_list': addr_list,
                      'num': num,
                      'gid_list_str': gid_list_str
                      }]
    return JsonResponse(response_data, safe=False)


def order_commit(request):
    '''
    提交订单
    addrId：地址ID
    pay_method：支付方式ID
    gid_list：商品ID集合  如4，3，2
    goods_order_total：商品订单总价
    carriage_price：运费
    goods_order_number：商品件数
    '''
    if request.method == 'POST':
        addrId = request.POST.get('addrId')
        pay_method = request.POST.get('pay_method')
        gid_list_str = request.POST.get('gid_list')
        goods_order_total = request.POST.get('goods_order_total')
        goods_order_number = request.POST.get('goods_order_number')
        print('goods_order_number', goods_order_number)
        carriage_price = request.POST.get('carriage_price')
        # 判断给的值
        if not all([addrId, pay_method, gid_list_str]):
            return JsonResponse({'status': '401', 'msg': '参数不完整'})
        # 构建订单id
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(request.user.id)
        print(order_id)
        # 设置事务保存点
        save_id = transaction.savepoint()
        print(save_id)
        try:
            order = Order.objects.create(order_id=order_id,
                                         user=request.user,
                                         address_id=addrId,
                                         pay_method=pay_method,
                                         goods_number=goods_order_number,
                                         goods_total=goods_order_total,
                                         carriage_price=carriage_price)
            gid_list = gid_list_str.split(',')
            for gid in gid_list:
                try:
                    # 获取购物车商品
                    cart = Cart.objects.get(goods_id=gid, user=request.user)
                    # 获取商品对象
                    goods = Goods.objects.get(pk=gid)
                except:
                    # 商品不存在
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'res': 4, 'errmsg': '商品不存在'})
                # 判断商品数量是否大于库存量
                if cart.number > goods.stock:
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'status': '401', 'msg': '库存不足'})

                print('order={},goods_id={},number={},price={}'.format(order_id, gid, cart.number, goods.price))

                # 添加订单商品
                OrderGoods.objects.create(order=order, goods_id=gid, number=cart.number, price=goods.price)
                # 修改商品库存
                goods.stock -= cart.number
                # 修改商品销量
                goods.sales += cart.number
                # 保存修改
                goods.save()

                # 删除购物车商品
                cart.delete()
        except Exception as err:
            transaction.savepoint_rollback(save_id)
            return JsonResponse({'status': '401', 'msg': '下单失败！'})

        # 提交事务
        transaction.savepoint_commit(save_id)

        return JsonResponse({'status': '200', 'msg': '下单成功！'})


def order_pay(request):
    '''
    订单支付
    orderId：订单ID
    '''
    order_id = request.POST.get('orderId')
    if not order_id:
        return JsonResponse({'status': '401', 'errmsg': '无效的订单编号!'})
    try:
        order = Order.objects.get(user=request.user, order_id=order_id, pay_method=2, order_status=1)
    except:
        return JsonResponse({'status': '401', 'errmsg': '订单错误！'})

    app_private_key_string = open(settings.PRIVATE_KEY).read()
    alipay_public_key_string = open(settings.PUBLIC_KEY).read()

    alipay = AliPay(
        appid="2021000116676798",  # 沙箱环境里的appid
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    # 如果你是 Python 3的用户，使用默认的字符串即可
    subject = "测试订单" + str(order_id)

    # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=str(order.goods_total),
        subject=subject,
        return_url=None,
        notify_url=None,  # 可选, 不填则使用默认notify url
    )

    # 支付宝网关
    url = 'https://openapi.alipaydev.com/gateway.do?'

    path = url + order_string
    return JsonResponse({'status': '200', 'pay_path': path})


def check_order(request):
    '''
    检查订单支付
    参数：
    orderId：订单ID
    '''
    order_id = request.POST.get('orderId')
    if not order_id:
        return JsonResponse({'status': '401', 'errmsg': '无效的订单编号!'})
    try:
        order = Order.objects.get(user=request.user, order_id=order_id, pay_method=2, order_status=1)
    except:
        return JsonResponse({'status': '401', 'errmsg': '订单错误！'})

    app_private_key_string = open(settings.PRIVATE_KEY).read()
    alipay_public_key_string = open(settings.PUBLIC_KEY).read()

    alipay = AliPay(
        appid="2021000116676798",  # 沙箱环境里的appid
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    while True:
        response = alipay.api_alipay_trade_query(order_id)
        code = response.get('code')
        trade_status = response.get('trade_status')
        if code == '10000' and trade_status == 'TRADE_STATUS':
            trade_no = response.get('trade_no')
            order.trade_no = trade_no
            order.order_status = 2
            order.save()
            return JsonResponse({'status': '200', 'msg': '支付成功！'})
        # 支付接口有问题，或者接口没有问题但是用户还没有支付成功
        elif code == '4000' or (code == '10000' and trade_status == 'WAIT_BUYER_PAY'):
            import time
            time.sleep(5)
            continue
        else:
            return JsonResponse({'status': '401', 'errmsg': '支付失败！'})


def order_comment(request):
    '''
    商品评论
    POST参数：
    order_id：订单ID
    total_count：订单有商品件数
    goods_1：订单商品ID
    content_1：评论内容
    GET参数：
    orderid：订单ID
    '''
    if request.method == 'POST':
        orderid = request.POST.get('order_id')
        if not orderid:
            return JsonResponse({'status': '401', 'msg': '订单错误！'})
        try:
            order = Order.objects.get(user=request.user, order_id=orderid)
        except:
            return JsonResponse({'status': '401', 'msg': '订单错误！'})
        count = int(request.POST.get('total_count'))  #订单中有几个商品
        for i in range(1, count + 1):
            ordergoods_id = request.POST.get('goods_' + str(i))  #订单商品
            comment = request.POST.get('content_' + str(i))  #评论1或评论2
            ordergoods = OrderGoods.objects.get(pk=ordergoods_id)
            ordergoods.comment = comment
            ordergoods.save()

        order.order_status = 5
        order.save()
        return JsonResponse({'status': '200', 'msg': '评价成功！'})

    else:
        orderid = request.GET.get('orderid')
        if not orderid:
            return JsonResponse({'status': '401', 'msg': '订单错误！'})
        try:
            order = Order.objects.get(user=request.user, order_id=orderid)
        except:
            return JsonResponse({'status': '401', 'msg': '订单错误！'})

        for status in Order.ORDER_STATUS:
            if order.order_status in status:
                order.status = status[1]
                break

        order_list = []
        order_list.append({'order_id': order.order_id, })

        ordergoods_list = []
        for ordergoods in order.ordergoods_set.all():
            ordergoods.total = ordergoods.price * ordergoods.number
            ordergoods_list.append({'name': ordergoods.goods.name, 'total': ordergoods.total})

        length = ordergoods_list.__len__()

        response_data = [{'order_list': order_list, 'ordergoods_list': ordergoods_list, 'length': length}]
        return JsonResponse(response_data,safe=False)
