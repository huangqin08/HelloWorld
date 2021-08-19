import datetime, uuid, requests
import json
import logging
import platform
import time

from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.utils.encoding import escape_uri_path

from ThinkJob.settings import URL, RESUME_FILE_URL, USER_CACHE_TIME, con, USER_DOWN_RESUME
from commer.CheckIP import checkip
from commer.CheckPhone import phone_check
from commer.CheckResumeCDVU import checkresume_cdvu
from commer.SysMemberUser import search_user
from commer.TodayResumeDownloads import today_resume_downloads
from resume.models import HrUserResumeRelation, HrResumeBase, HrTempBase
from userhr.models import SysMember, SysMemberOpthistory, HrResumeAlarm

from django.middleware.csrf import get_token

from userhr.modelserializer import SysMemberSerializer, UpdateUserListSerializer

logger = logging.getLogger('log')


def test(request):
    con.set('{}:{}'.format('2020-09-28', 'beeaba1af40f11ea847300163e086b6a'), 201, 60 * 60 * 8)
    # obj_all = HrResumeBase.objects.all()
    # for i in obj_all:
    #     if i.pdf_url:
    #         pdf_url = i.pdf_url
    #         i.pdf_url = pdf_url.replace("https://job.thinkyun.cn", "https://www.thinkjob.com");
    #         i.save()

    # list = ["游戏", "电商", "金融", "教育", "文化娱乐", "本地生活", "硬件制造", "旅游", "物流", "社交", "地图", "信息安全", "企业服务", "医疗健康",
    #         "汽车", "招聘", "即时通讯", "广告营销", "大数据", "云计算", "房产服务", "移动互联网", "工具软件", "体育运动", "不限"]
    # create_time = '2020-09-09 16:07:53'
    #
    # for k, v in enumerate(list):
    #     SysCodes.objects.create(id=str(k + 59), code='0' + str(k + 1), name=v, dtype='trade', integral=0, status='1',
    #                             create_time=create_time, create_psn='admin')
    return JsonResponse({})
    # return render(request, 'xsl_update.html')


# 用户在线状态检测
def checkuser_login(request):
    if request.method == 'GET':
        uid = request.GET.get('uid')

        server_session = con.get('user:' + uid)
        if not server_session:
            return JsonResponse({'status': 201, 'msg': '用户未登录', 'data': {}})

        status = eval(server_session)
        logger.info('该用户{}的状态为：{}'.format(uid, status))
        if status == 0:
            return JsonResponse({'status': 409, 'msg': '帐号已冻结', 'data': {}})

        session = cache.get('user_session:' + uid)
        if not (session == request.COOKIES['session']):
            logger.info('您的帐号已经在其他地方登录')
            return JsonResponse({'status': 203, 'msg': '您的帐号已经在其他地方登录', 'data': {}})

        return JsonResponse({'status': 200, 'msg': '该帐号状态正常', 'data': {}})


# token令牌获取方式
def token(request):
    token = get_token(request)
    response = HttpResponse(json.dumps({'token': token}), content_type="application/json,charset=utf-8")
    # response_data = {
    #     'status': 200,
    #     'msg': 'token信息获取成功',
    #     'token': token
    # }
    return response


# 用户上传列表
def userupdate_list(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        page = request.POST.get('page')
        page_size = request.POST.get('page_size', 10)

        resumebase = HrResumeBase.objects.filter(up_user_id=uid).order_by('-create_time')
        tempbase = HrTempBase.objects.filter(up_user_id=uid).order_by('-create_time')

        # 将查询到的2组数据通过list的特性进行合并
        all_things = list(resumebase) + list(tempbase)
        logger.debug('用户上传了{}封简历'.format(all_things.__len__()))

        if all_things.__len__() == 0:
            return JsonResponse({'status': 302, 'msg': '该用户没有上传过'})

        # 然后将合并后的数据进行update_time参数的降序排列
        sorted_things = sorted(all_things, key=lambda x: x.create_time, reverse=True)

        # 实例化一个分页组件，第一个参数是需要被分页的列表，第二个参数是每一个的item个数，比如这边指定每页个数为page_size
        paginator = Paginator(sorted_things, page_size)
        if paginator.num_pages < int(page):
            return JsonResponse({'status': 300, 'msg': '分页超出最大值'})

        # page方法，传入一个参数，表示第几页的列表，这边传入的page，是你在地址中写的参数，传入page后返回该页面的所有数据page_article_list
        page_article_list = paginator.page(page)

        list_obj = UpdateUserListSerializer(page_article_list, many=True)

        # 创建一个空列表去装载数据
        list_detail = []

        for i in list_obj.data:
            resume_use = {}
            for k, v in i.items():
                resume_use[k] = '' if v == None else v
            list_detail.append(resume_use)

        # 准备给前端返回的数据信息
        response_data = {
            'status': 200,
            'msg': '数据查询成功',
            'data': {
                'page': page,
                'page_size': page_size,
                'count': all_things.__len__(),
                'page_amount': str(paginator.num_pages),
                'list_detail': list_detail,
            }
        }

    return JsonResponse(response_data)


# 用户登录
def user_login(request):
    if request.method == 'POST':
        # 获取用户手机号
        phone = request.POST.get('phone')
        # 获取密码
        user_pwd = request.POST.get('user_pwd')
        # 获取验证码
        img_code = request.POST.get('img_code')

        try:
            cookie_img_code = request.COOKIES['CODE']
            logger.info('从cookie中拿到的值为：{}'.format(cookie_img_code))
        except:
            return JsonResponse({'status': 204, 'msg': '验证码错误'})

        redis_img_code = cache.get('IMG_CODE:' + cookie_img_code)
        logger.info('从redis中拿到的值为：{}'.format(redis_img_code))
        if not redis_img_code:
            logger.info('用户使用了错误的验证码，为了安全删除之前的验证码')
            cache.delete('IMG_CODE:' + cookie_img_code)
            return JsonResponse({'status': 204, 'msg': '验证码错误'})

        # 从浏览器的cookie中拿到CODE，用CODE来去redis中获取验证码
        # try:
        #     session_img_code = request.session['CODE']
        #     logger.info('从session中拿到的值为：{}'.format(session_img_code))
        # except:
        #     logger.error('COOKIES中没有IME_CODE')
        #     return JsonResponse({'status': 204, 'msg': '验证码错误'})

        # redis_img_code = cache.get('IME_CODE:' + cookies_img_code)
        # logger.info('从redis中拿到的验证码为：{}'.format(redis_img_code))
        # if not redis_img_code:
        #     return JsonResponse({'status': 204, 'msg': '验证码错误'})

        if not (img_code.lower() == redis_img_code.lower()):
            logger.info('用户使用了错误的验证码，为了安全删除之前的验证码')
            cache.delete('IMG_CODE:' + cookie_img_code)
            return JsonResponse({'status': 204, 'msg': '验证码错误'})
        else:
            logger.info('redis中的验证码为：{} ，用户提交的验证码为：{}'.format(redis_img_code, img_code))

        logger.info('用户手机号为--------->{}'.format(phone))
        # 从数据库中查询该用户对象
        user = search_user(phone=phone)

        if not user:
            return JsonResponse({'status': 403, 'msg': '无此用户或用户未注册', 'data': {}})

        if user.status == '0':
            return JsonResponse({'status': 409, 'msg': '帐号已冻结', 'data': {}})

        logger.info('搜索用户对象--------->{}'.format(user.user_name))
        # 校验用户密码是否正确
        if check_password(user_pwd, user.user_pwd):
            logger.info('用户登录成功，为了安全删除之前的验证码')
            cache.delete('IMG_CODE:' + cookie_img_code)
            # 用户登录成功之后将用户的uuid信息记录到服务器的redis信息中用于校验用户登录状态
            logger.info('用户登录成功,将用户的uuid信息设置到redis中,用户的redis缓存信息为：{}'.format(user.id))
            ip = checkip(request)
            user.last_ip = ip
            user.session = str(uuid.uuid1().hex)
            user.save()

            data = {'userid': user.id, 'user_name': '' if user.user_name == None else user.user_name,
                    'company_name': user.company_name,
                    'phone': user.phone}
            # 准备给前端返回的数据信息
            response_data = {
                'status': 200,
                'msg': '用户登录成功',
                'data': data
            }
            con.set('user:' + user.id, 1, USER_CACHE_TIME)  # 将用户的信息设置到redis中
            cache.set('user_session:' + user.id, user.session, USER_CACHE_TIME)
            response = JsonResponse(response_data)
            response.set_cookie('session', user.session)
        else:
            logger.info('用户密码核验--------->{}'.format('密码错误'))
            # 准备给前端返回的数据信息
            response_data = {
                'status': 400,
                'msg': '用户名或密码错误',
                'data': {}
            }
            response = JsonResponse(response_data)
        return response


# 短信登录
def message_login(request):
    if request.method == 'POST':
        # 获取用户手机号
        phone = request.POST.get('phone')
        message_code = request.POST.get('message_code')
        logger.info('用户登录手机号为--------->{}'.format(phone))

        # 提取用户验证码，如果无法正常从缓存中提取验证码，说明验证码过期或者验证码错误
        cache_phone_message = cache.get('phone_message:' + phone)
        logger.info('用户提交的验证码信息------->{}'.format(message_code))
        logger.info('通过{}手机号取出的缓存验证码------->{}'.format(phone, str(cache_phone_message)))

        if cache_phone_message == None or (not (message_code in str(cache_phone_message))):
            return JsonResponse({'status': 406, 'msg': '验证码错误'})

        # 查询该用户对象
        user = search_user(phone=phone)

        if not user:
            logger.info('搜索用户对象--------->None')
            return JsonResponse({'status': 403, 'msg': '无此用户或用户未注册', 'data': {}})

        if user.status == '0':
            return JsonResponse({'status': 409, 'msg': '帐号已冻结', 'data': {}})

        ip = checkip(request)
        user.last_ip = ip
        user.session = str(uuid.uuid1().hex)
        user.save()
        data = {'userid': user.id, 'user_name': user.user_name, 'company_name': user.company_name,
                'phone': user.phone, 'status': user.status}

        # 确认到用户存在并且验证码校验通过后，可以提示用户登录成功了
        logger.info('用户登录成功,将用户的uuid信息设置到redis中,用户的redis为：{}'.format(user.id))
        con.set('user:' + user.id, 1, USER_CACHE_TIME)  # 将用户的信息设置到redis中
        cache.set('user_session:' + user.id, user.session, USER_CACHE_TIME)
        # 准备给前端返回的数据信息
        response_data = {
            'status': 200,
            'msg': '用户登录成功',
            'data': data
        }
        response = JsonResponse(response_data)
        response.set_cookie('session', user.session)
        return response


# 用户注销
def user_logout(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        uid_r = con.get('user:' + uid)
        # 用户需要注销登录了，确定redis中有这个用户的基本数据
        logger.info('{}用户要注销登录了，redis的数据检查为：{}'.format(uid, uid_r))
        if uid_r:
            con.delete('user:' + uid)
        logger.info('此{}用户需要注销成功'.format(uid))
    return JsonResponse({'status': 200, 'msg': '操作成功'})


# 修改密码
def checkpassword(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        logger.info('该{}用户需要修改密码'.format(uid))

        user_pwd_new = request.POST.get('user_pwd_new')
        user_pwd_old = request.POST.get('user_pwd_old')
        user = search_user(uid=uid)

        logger.info('需要对数据库原始密码进行核验')
        if check_password(user_pwd_old, user.user_pwd):
            logger.info('核验成功，{}用户可以修改密码'.format(uid))
            user.user_pwd = make_password(user_pwd_new)
            user.save()
            logger.info('用户修改过密码，删除缓存')

            response_data = {
                'status': 200,
                'msg': '密码修改成功',
                'data': {
                    'userid': user.id,
                    'user_name': user.user_name,
                    'company_name': user.company_name,
                    'phone': user.phone,
                }
            }
            return JsonResponse(response_data)
        else:
            logger.info('核验失败，{}用户原密码错误'.format(uid))
            return JsonResponse({'status': 402, 'msg': '密码修改失败或原密码错误', 'data': {}})


# 用户忘记密码
def forget_pwd(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        user_pwd_new = request.POST.get('user_pwd_new')
        message_code = request.POST.get('message_code')

        # 提取用户验证码，如果无法正常从缓存中提取验证码，说明验证码过期或者验证码错误
        cache_phone_message = cache.get('phone_message:' + phone)
        logger.info('用户提交的验证码信息------->{}'.format(message_code))
        logger.info('通过{}手机号取出的缓存验证码------->{}'.format(phone, str(cache_phone_message)))

        if cache_phone_message == None or (not (str(cache_phone_message) in message_code)):
            return JsonResponse({'status': 406, 'msg': '验证码错误'})

        user = search_user(phone=phone)
        logger.info('验证码通过校验，准备修改{}用户的密码，此用户注册的手机号为{}'.format(user.id, phone))

        user.user_pwd = make_password(user_pwd_new)
        logger.info('密码加密完成，已经修改成功，删除缓存数据')
        user.save()

        return JsonResponse({'status': 200, 'msg': '密码修改成功'})


# 校验手机号能否注册
def checkphone(request):
    logger.info('收到一个用户请求--------->{}'.format(request.method))
    phone = request.GET.get('phone')
    logger.info('需要校验的手机号--------->{}'.format(phone))
    userphone = phone_check(phone)
    logger.info('校验结果--------->{}'.format(userphone))
    if not userphone:
        response_data = {
            'status': 401,
            'msg': '该手机号已被注册'
        }
    else:
        response_data = {
            'status': 200,
            'msg': '手机号可以注册'
        }
    return JsonResponse(response_data)


# 用户注册
def register(request):
    if request.method == 'POST':
        # 设置UUID随机作为用户ID，用户提交的登录信息
        id = str(uuid.uuid1().hex)
        phone = request.POST.get('phone')
        user_pwd = request.POST.get('user_pwd')
        company_name = request.POST.get('company_name')
        message_code = request.POST.get('message_code')

        # 首先检查该手机号是否被注册过
        userphone = phone_check(phone)
        logger.info('这个用户能否注册--------->{}'.format(userphone))
        if not userphone:
            return JsonResponse({'status': 401, 'msg': '该手机号以被注册', 'data': {}})

        # 提取用户验证码，如果无法正常从缓存中提取验证码，说明验证码过期或者验证码错误
        cache_phone_message = cache.get('phone_message:' + phone)
        logger.info('用户提交的验证码信息------->{}'.format(message_code))
        logger.info('通过{}手机号取出的缓存验证码------->{}'.format(phone, str(cache_phone_message)))

        if cache_phone_message == None or (not (message_code in str(cache_phone_message))):
            return JsonResponse({'status': 406, 'msg': '验证码错误'})

        # 服务器设置一些基本信息
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')  # 创建时间
        create_psn = phone  # 创建人

        '''
        user_name = request.POST.get('user_name')
        
        link_name = request.POST.get('link_name')
        company_scale = request.POST.get('company_scale')
        e_mail = request.POST.get('e_mail')
        content = request.POST.get('content')
        attention_key = request.POST.get('attention_key')
        integral = request.POST.get('integral')
        status = request.POST.get('status')
        last_ip = request.POST.get('last_ip')
        last_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        photo_url = request.FILES.get('photo_url')
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        create_psn = request.POST.get('create_psn')
        update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        update_psn = request.POST.get('update_psn')
        user_level = request.POST.get('user_level')
        '''

        logger.info('用户密码加密开始')
        user_pwd = make_password(user_pwd)
        logger.info('用户密码加密结束：{}'.format(user_pwd))

        logger.info('创建用户数据库保存对象')
        user = SysMember()
        user.id = id
        user.integral = 100
        user.user_pwd = user_pwd
        user.company_name = company_name
        user.create_psn = create_psn
        user.create_time = create_time
        user.status = 1
        user.phone = phone
        user.save()
        logger.info('用户创建成功------->{}'.format(id))

        response_data = {
            'status': 200,
            'msg': '注册成功',
            'data': {
                'userid': id,
                'phone': phone,
                'company_name': company_name,
            }
        }
        user_session = str(uuid.uuid1().hex)
        con.set('user:' + user.id, 1, USER_CACHE_TIME)  # 将用户的信息设置到redis中
        cache.set('user_session:' + user.id, user_session, USER_CACHE_TIME)
        response = JsonResponse(response_data)
        response.set_cookie('session', user_session)

        logger.info('用户创建成功------->{}'.format(response_data))
        return response


# 用户详情获取
def detail_user(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        logger.info('需要查询的用户uid--------->{}'.format(uid))
        user = search_user(uid=uid)
        if not user:
            logger.info('查询结果--------->{}'.format('无此用户数据'))
            return JsonResponse({'status': 403, 'msg': '无此用户数据', 'data': {}})

        logger.info('查询结果--------->{}'.format(user.id))

        user_s = SysMemberSerializer(user)
        list = {}
        for k, v in user_s.data.items():
            list[k] = '' if v == None else v

        return JsonResponse({'status': 200, 'msg': '成功获取用户数据', 'data': list})


# 用户编辑
def editor_user(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')  # 用户的uuid信息
        # phone = request.POST.get('phone') #用户手机号
        user_name = request.POST.get('user_name')  # 用户名
        company_name = request.POST.get('company_name')  # 企业名称
        link_name = request.POST.get('link_name')  # 联系人
        company_scale = request.POST.get('company_scale')  # 公司规模
        e_mail = request.POST.get('e_mail')  # 企业邮箱
        content = request.POST.get('content')  # 公司介绍
        attention_key = request.POST.get('attention_key')  # 热门关注
        update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')  # 更新时间
        update_psn = request.POST.get('user_name')  # 更新人
        company_trade = request.POST.get('company_trade')

        user = search_user(uid=uid)
        if user:
            logger.info('查询用户成功--------->{}'.format(user.id))
            user.user_name = user_name
            user.company_name = company_name
            user.link_name = link_name
            user.company_scale = company_scale
            user.e_mail = e_mail
            user.content = content
            user.attention_key = attention_key
            user.update_time = update_time
            user.update_psn = update_psn
            user.company_trade = company_trade
            user.save()
            logger.info('用户已经修改过详情数据了，删除缓存')

            response_data = {
                'status': 200,
                'msg': '修改成功',
                'data': {
                    'userid': user.id,
                    'user_name': '' if user.user_name == None else user.user_name,
                    'company_name': user.company_name,
                    'phone': user.phone,
                }
            }
            return JsonResponse(response_data)
        else:
            logger.info('查询用户失败--------->')
            return JsonResponse({'status': 403, 'msg': '无此用户数据', 'data': {}})


# 简历上传
def resume_update(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        file_list = request.FILES.getlist('files')
        resume_time_strptime = request.POST.get('resume_time')
        timeStamp = float(int(resume_time_strptime) / 1000)
        timeArray = time.localtime(timeStamp)
        resume_time = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)

        logger.info('开始时间转换：{}转换{}'.format(resume_time_strptime, resume_time))

        logger.info('用户{}上传了{}份简历'.format(uid, file_list.__len__()))

        if file_list.__len__() <= 0 or file_list == None:
            return JsonResponse({'status': 407, 'msg': '上传文件不得少于1个'})

        # 设置一个数组，重组多文件上传命名格式
        file_list_ = []
        for i in file_list:
            logger.info('用户{}上传了{}简历'.format(uid, i))
            file_list_.append(('files', i))

        logger.info('用户上传的简历格式为：{}'.format(file_list_))

        # java处理文件接口服务器
        logger.info('打印上传服务器的基本信息，服务器的ip：{}，上传用户：{}'.format(URL, uid))
        response = requests.post(url=URL, data={'uid': uid, 'lastModifiedTime': resume_time}, files=file_list_)

        try:
            json_date_e = response.json()
            logger.info('简历解析服务器返回的信息：{}'.format(json_date_e))

            if not (json_date_e['result'] in 'success'):
                return JsonResponse({'status': 500, 'msg': '服务器内部错误'})
            else:
                return JsonResponse({'status': 200, 'msg': '上传成功'})

        except Exception as e:
            logger.error('这里发生了一个错误：{}'.format(e))


# 用户收藏
def user_collect(request):
    if request.method == 'POST':
        id = str(uuid.uuid1().hex)
        uid = request.POST.get('uid')
        resume_id = request.POST.get('resume_id')
        type = 'collect'
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        logger.info('{}用户要收藏简历了'.format(uid))

        # 开始检查简历是否存在
        resume_id_ = HrResumeBase.objects.filter(id=resume_id).first()
        if not resume_id_:
            logger.info('用户收藏了一个{}无效简历'.format(resume_id))
            return JsonResponse({'status': 803, 'msg': '这不是个有效的简历'})

        usercollect = HrUserResumeRelation.objects.filter(uid=uid, resume_id=resume_id, type=type).first()
        if usercollect:
            logger.info('{}用户已经收藏过{}简历了，现在取消收藏'.format(uid, resume_id))
            usercollect.delete()
            return JsonResponse({'status': 200, 'msg': '取消收藏成功'})

        usercollect = HrUserResumeRelation()
        usercollect.id = id
        usercollect.uid = uid
        usercollect.resume_id = resume_id
        usercollect.type = type
        usercollect.integral = 0
        usercollect.create_time = create_time
        usercollect.save()
        logger.info('{}用户已成功收藏该{}简历，当前收藏编号：{}'.format(uid, resume_id, id))

        response_data = {
            'status': 200,
            'msg': '收藏成功',
            'data': {
                'id': str(usercollect),
                'uid': str(usercollect.uid),
                'resume_id': str(usercollect.resume_id),
            }
        }
        return JsonResponse(response_data)


# 收藏下载状态查询
def colldown_status(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        resume_id = request.POST.get('resume_id')
        logger.info('{}用户要查询这个{}简历的状态了'.format(uid, resume_id))
        data_status = checkresume_cdvu(uid, resume_id)
        return JsonResponse({'status': 200, 'msg': '状态查询成功', 'data': data_status})


# 用户数据统计
def user_datastatis(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        logger.info('需要统计该{}用户的一些基本数据了'.format(uid))

        all_integral_num = SysMember.objects.filter(id=uid).first()
        if not all_integral_num:
            logger.info('没有找到该{}用户'.format(uid))
            return JsonResponse({'status': 403, 'msg': '未查询到相关的用户信息或无此用户'})
        else:
            all_integral_num = all_integral_num.integral
            logger.info('该{}用户的总积分为：{}'.format(uid, all_integral_num))

        # 获取用户的上传简历数
        updata_resume_num = HrResumeBase.objects.filter(up_user_id=uid).count()
        tempbase_resume_num = HrTempBase.objects.filter(up_user_id=uid).count()
        logger.info('该{}用户的上传简历数为：{}'.format(uid, updata_resume_num + tempbase_resume_num))

        # 用户的下载简历数
        download_resume_num = HrUserResumeRelation.objects.filter(uid=uid, type='down').count()
        logger.info('该{}用户的下载简历数为：{}'.format(uid, download_resume_num))

        # 用户的消费积分
        user_point_int = HrUserResumeRelation.objects.filter(uid=uid).filter(Q(type='down') | Q(type='view')).all()
        point_int = 0
        for k in user_point_int:
            point_int += k.integral
        logger.info('该{}用户的消费积分为：{}'.format(uid, point_int))

        # 用户的上传积分
        user_upload_int = HrUserResumeRelation.objects.filter(uid=uid, type='upload').all()
        up_int = 0
        for k in user_upload_int:
            up_int += k.integral
        logger.info('该{}用户的上传获得的积分为：{}'.format(uid, up_int))

        # 企业排名
        cp_rankings = HrUserResumeRelation.objects.filter(type='upload').values('uid').annotate(
            counts=Count(id)).order_by('-counts')
        cor_rankings = '--'
        for k, v in enumerate(cp_rankings):
            if uid == v['uid']:
                cor_rankings = k + 1

        # 用户当日下载数据统计
        num = today_resume_downloads(uid)

        response_data = {
            'status': 200,
            'msg': '用户数据统计成功',
            'data': {
                'updata_resume_num': updata_resume_num + tempbase_resume_num,
                'download_resume_num': download_resume_num,
                'all_integral_num': 0 if all_integral_num == None else all_integral_num,
                'point_int': point_int,
                'up_int': up_int,
                'cor_rankings': cor_rankings,
                'use_download_num': num,
            }
        }
        return JsonResponse(response_data)


# 用户下载简历
def download_file(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')  # 用户uuid
        resume_id = request.POST.get('resume_id')  # 简历id
        download_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 记录用户下载时间

        logger.info('{}用户在{}下载了{}简历'.format(uid, download_time, resume_id))

        user = SysMember.objects.get(id=uid)
        if not user:
            logger.info('在数据库中未查到该用户{}'.format(uid))
            return JsonResponse({'status': 403, 'msg': '未查询到相关的用户信息或无此用户'})

        resume = HrResumeBase.objects.filter(id=resume_id).first()
        if not resume:
            logger.info('在数据库中未找到这份简历{}'.format(resume_id))
            return JsonResponse({'status': 803, 'msg': '这不是个有效的简历'})

        if not resume.integral:
            logger.info('在数据库中未找到这份简历{}的分值数据，需要管理员处理'.format(resume_id))
            return JsonResponse({'status': 500, 'msg': '内部服务器错误'})

        # 用户积分可用的情况下判断用户是否有历史下载记录，有的话默认就不插入数据
        # usercollect = HrUserResumeRelation.objects.filter(uid=uid, resume_id=resume_id).filter(
        #     Q(type='down') | Q(type='view')).first()

        data_status = checkresume_cdvu(uid, resume_id)

        if data_status['down'] and data_status['view']:
            logger.info('用户{}查看并下载过该{}简历，【无需二次记录】'.format(uid, resume_id))
        else:
            if not data_status['down']:
                usercollect = HrUserResumeRelation()
                usercollect.id = str(uuid.uuid1().hex)
                usercollect.uid = uid
                usercollect.resume_id = resume_id
                usercollect.type = 'down'
                if not data_status['view']:
                    # 在准备扣取积分之前判断用户是否达到当日下载简历上限
                    num = today_resume_downloads(uid)
                    if num > USER_DOWN_RESUME:
                        return JsonResponse({'status': 412, 'msg': '已达到当然200封简历（下载或查看）上限，请明天下载'})
                    else:
                        today_resume_downloads(uid, 'set')

                    # 用户即没有查看也没有下载，那么在扣积分之前检查用户积分时候充足
                    if user.integral == None or user.integral < resume.integral:
                        logger.info('用户可用积分为：{}，积分不足无法下载'.format(user.integral))
                        return JsonResponse({'status': 408, 'msg': '可用积分不足'})

                    logger.info('用户并未{}查看和下载过该{}简历，开始扣分操作'.format(uid, resume_id))
                    # 将本次的扣分记录到库中
                    usercollect.integral = -resume.integral
                    # 对用户的总分进行扣取
                    user.integral = user.integral - resume.integral
                    user.save()
                    logger.info('{}用户积分已扣取,目前剩余积分为：{}'.format(uid, user.integral))

                    # 开始记录积分轨迹
                    opt_create = SysMemberOpthistory()
                    opt_create.id = str(uuid.uuid1().hex)
                    opt_create.uid = uid
                    opt_create.opt_type = 'down'
                    opt_create.opt_cnt = 1
                    opt_create.cur_integral = -resume.integral
                    opt_create.total_integral = user.integral
                    opt_create.memo = '简历下载积分扣取'
                    opt_create.create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 创建时间
                    opt_create.save()
                    logger.info('本次{}用户下载{}简历的轨迹信息已记录'.format(uid, resume_id))
                else:
                    logger.info('用户{}查看过该{}简历，本次下载不扣积分'.format(uid, resume_id))
                    usercollect.integral = 0
                usercollect.create_time = download_time
                usercollect.save()

        file_name = resume.name
        logger.info('用户{}下载的文件为：{}'.format(uid, file_name))

        def file_iterator(file_path, chunk_size=512):
            """
            文件生成器,防止文件过大，导致内存溢出
            :param file_path: 文件绝对路径
            :param chunk_size: 块大小
            :return: 生成器
            """
            with open(file_path, mode='rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        file_url = resume.file_url.split('uploadFiles')

        try:
            # 设置响应头
            # StreamingHttpResponse将文件内容进行流式传输，数据量大可以用这个方法
            if platform.system() == 'Linux':
                response = StreamingHttpResponse(file_iterator(RESUME_FILE_URL + file_url[1]))
                # 以流的形式下载文件,这样可以实现任意格式的文件下载
                response['Content-Type'] = 'application/octet-stream'
                # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
                response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                response['Content-Disposition'] = 'attachment;{};{}'.format(escape_uri_path(
                    file_name), file_url[1].split('.')[1])
                logger.info('{}文件已完成下载'.format(file_name + '.' + file_url[1].split('.')[1]))
            else:
                logger.info('windows测试环境不直接下载')
                logger.info('{}文件已完成下载'.format(file_name + '.' + file_url[1].split('.')[1]))
                return JsonResponse({'status': 200, 'msg': 'windows测试环境不直接下载'})

        except Exception as e:
            print(e)
            logger.error('服务器下载行为出错，错误为：'.format(e))
            return JsonResponse({'status': 500, 'msg': '内部服务器错误'})

        return response


# 简历联系方式查看
def look_resume(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')  # 用户uuid
        resume_id = request.POST.get('resume_id')  # 简历id
        check_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        logger.info('用户{}在【{}】查看了该{}简历的联系方式'.format(uid, check_time, resume_id))

        user = SysMember.objects.get(id=uid)
        if not user:
            logger.info('系统校验到没有这个用户{}'.format(uid))
            return JsonResponse({'status': 403, 'msg': '未查询到相关的用户信息或无此用户'})

        resume = HrResumeBase.objects.filter(id=resume_id).first()
        if not resume:
            logger.info('这是一个无效{}简历，用户无法收藏'.format(uid, resume_id))
            return JsonResponse({'status': 803, 'msg': '这不是个有效的简历'})

        if not resume.integral:
            logger.info('在数据库中未找到这份简历{}的分值数据，需要管理员处理'.format(resume_id))
            return JsonResponse({'status': 500, 'msg': '内部服务器错误'})

        # 检查用户是否操作过该简历
        # usercollect = HrUserResumeRelation.objects.filter(uid=uid, resume_id=resume_id).filter(
        #     Q(type='view') | Q(type='down')).first()
        data_status = checkresume_cdvu(uid, resume_id)

        if data_status['down'] and data_status['view']:
            logger.info('用户{}查看并下载过该{}简历，【无需二次记录】'.format(uid, resume_id))
        else:
            if not data_status['view']:
                usercollect = HrUserResumeRelation()
                usercollect.id = str(uuid.uuid1().hex)
                usercollect.uid = uid
                usercollect.resume_id = resume_id
                usercollect.type = 'view'
                if not data_status['down']:
                    # 在准备扣取积分之前判断用户是否达到当日下载简历上限
                    num = today_resume_downloads(uid)
                    if num > USER_DOWN_RESUME:
                        return JsonResponse({'status': 412, 'msg': '已达到当然200封简历（下载或查看）上限，请明天下载'})
                    else:
                        today_resume_downloads(uid, 'set')

                    # 在简历没有查看也没有下载的状态下进行积分是否充足的判断
                    if user.integral == None or user.integral < resume.integral:
                        logger.info('用户可用积分为：{}，无法查看简历的联系方式'.format(user.integral))
                        return JsonResponse({'status': 408, 'msg': '可用积分不足'})

                    logger.info('用户并未{}查看和下载过该{}简历，开始扣分操作'.format(uid, resume_id))
                    # 将本次的扣分记录到库中
                    usercollect.integral = -resume.integral
                    # 对用户的总分进行扣取
                    user.integral = user.integral - resume.integral
                    user.save()
                    logger.info('{}用户积分已扣取,目前剩余积分为：{}'.format(uid, user.integral))

                    # 开始记录积分轨迹
                    opt_create = SysMemberOpthistory()
                    opt_create.id = str(uuid.uuid1().hex)
                    opt_create.uid = uid
                    opt_create.opt_type = 'view'
                    opt_create.opt_cnt = 1
                    opt_create.cur_integral = -resume.integral
                    opt_create.total_integral = user.integral
                    opt_create.memo = '联系方式查看积分扣取'
                    opt_create.create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 创建时间
                    opt_create.save()
                    logger.info('本次{}用户查看{}简历的轨迹信息已记录'.format(uid, resume_id))
                else:
                    logger.info('用户{}下载过该{}简历，本次查看不扣积分'.format(uid, resume_id))
                    usercollect.integral = 0
                usercollect.create_time = check_time
                usercollect.save()

        response_data = {
            'status': 200,
            'msg': '查询成功',
            'data': {
                'resume_id': resume_id,
                'phone': resume.phone,
                'e_mail': resume.e_mail,
                'name': resume.name,
            }
        }
        return JsonResponse(response_data)


# 用户反馈信息表
def user_alarm(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        resume_id = request.POST.get('resume_id')
        chk_phone = request.POST.get('chk_phone')
        chk_work = request.POST.get('chk_work')
        memo = request.POST.get('memo')
        appraise = request.POST.get('appraise')

        if not any([chk_phone, chk_work, memo, appraise]):
            logger.info('并未提交任何有用的反馈信息，不做入库处理')
            return JsonResponse({'status': 413, 'msg': '并未提交任何有用的反馈信息'})

        if appraise and appraise.__len__()<2000:
            HrResumeBase.objects.filter(id=resume_id).update(memo=appraise)
        else:
            return JsonResponse({'status': 410, 'msg': '提交内容超出限制'})

        send_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')  # 创建时间

        if memo is not None and memo.__len__() > 500:
            return JsonResponse({'status': 410, 'msg': '提交内容超出限制'})

        logger.info('已经有用户{}提交该简历{}的反馈信息'.format(uid, resume_id))
        # 需要检查这个简历是否存在
        base_obj = HrResumeBase.objects.filter(id=resume_id).first()
        if not base_obj:
            return JsonResponse({'status': 803, 'msg': '这不是个有效的简历'})

        # 开始检查之前是否提交过反馈，防止用户二次提交
        list_obj = HrResumeAlarm.objects.filter(send_user_id=uid, pk_id=resume_id).first()
        if list_obj:
            return JsonResponse({'status': 410, 'msg': '已经对该简历提交过反馈信息，请勿重复操作'})

        create_obj = HrResumeAlarm()
        create_obj.send_user_id = uid
        create_obj.pk_id = resume_id
        create_obj.chk_phone = chk_phone
        create_obj.chk_work = chk_work
        create_obj.memo = memo
        create_obj.send_time = send_time
        create_obj.save()
        return JsonResponse({'status': 200, 'msg': '我们已成功收到您的反馈信息，非常感谢'})
