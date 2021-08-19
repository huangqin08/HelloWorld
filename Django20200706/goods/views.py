from django.http import HttpResponse, JsonResponse

# Create your views here.
from Django20200706.settings import MEDIA_URL
from cart.models import Cart
from goods.models import GoodsType, IndexSaleBanner, IndexGoodsBanner, IndexGoodsTypeBanner, Goods

def index(request):
    '''商城首页'''
    # 商品类型的展示
    types = GoodsType.objects.all()
    types_list = []
    for type in types:
        types_list.append({'name':type.name,'image':MEDIA_URL+str(type.image),'logo':type.logo})
    # 轮播图的展示
    banners = IndexGoodsBanner.objects.all().order_by('index')
    banners_list = []
    for banner in banners:
        banners_list.append({'goods':banner.goods.name,'image':MEDIA_URL+str(banner.image)})
    # 促销商品的展示
    sales = IndexSaleBanner.objects.all().order_by('index')
    sales_list = []
    for sale in sales:
        sales_list.append({'name': sale.name, 'image':MEDIA_URL+str(sale.image),'url':sale.url})
    # 标题和图片广告商品的展示
    image_list=[]
    title_list = []
    for type in types:
        #图片类的展示商品
        image_adv = IndexGoodsTypeBanner.objects.filter(type=type,display_type=1).order_by('index')
        #标题类的展示商品
        title_adv = IndexGoodsTypeBanner.objects.filter(type=type,display_type=0).order_by('index')
        #动态添加属性
        type.image_adv = image_adv
        type.title_adv = title_adv

        for image in type.image_adv:
            image_list.append({'typeID':image.type.id,'name': image.goods.name,'image':MEDIA_URL+str(image.goods.image),'price':image.goods.price,'goodsID':image.goods.id})
        for title in type.title_adv:
            title_list.append({'name': title.goods.name,'goodsID':title.goods.id})
    #查询这个用户下购物车的数量
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).count()

    response_data = {
        'types_list':types_list,
        'banners_list':banners_list,
        'sales_list': sales_list,
        'image_list':image_list,
        'title_list':title_list,
        'count':count
    }
    return JsonResponse(response_data)


def goods_detail(request,gid):
    '''商品详情页'''

    try:  #万一传的gid有错的话就try一下
        # 通过gid获取商品
        goods = Goods.objects.get(pk=gid)
    except:
        return HttpResponse('商品详情的gid有错误！')

    goodss =[{'name':goods.name,
                 'type':goods.type.name,
                 'image':MEDIA_URL+str(goods.image),
                 'desc':goods.desc,
                 'price':goods.price,
                 'unite':goods.unite,
                 'detail':goods.detail}]
    #商品详情的图片
    GoodsImage = goods.goodsimage_set.all()
    GoodsImage_list = []
    for pics in GoodsImage:
        GoodsImage_list.append({'goodsdetail':MEDIA_URL+str(pics.image)})

    #商品类别
    types = GoodsType.objects.all()
    types_list = []
    for type in types:
        types_list.append({'name': type.name})

    #新品推荐
    new_goods = Goods.objects.filter(type=goods.type).order_by('-add_time')[:2]
    new_goods_list=[]
    for goods in new_goods:
        new_goods_list.append({'name':goods.name,'image':MEDIA_URL+str(goods.image),'price':goods.price})

    #查询这个用户下购物车的数量
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).count()

    response_data = {'types_list':types_list,
                     'goodss':goodss,
                     'new_goods_list':new_goods_list,
                     'GoodsImage_list':GoodsImage_list,
                     'count':count}
    return JsonResponse(response_data)

