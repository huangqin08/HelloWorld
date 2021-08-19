#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   login_middleware.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/7/30 13:03   gxrao      1.0         None
'''
import logging

from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

# 以下是需要鉴权登录的地址
from ThinkJob.settings import con, USER_CACHE_TIME

# loginRequired_list = ['/userhr/editor_user', '/userhr/detail_user', '/userhr/checkpassword', '/userhr/resume_update'
#     , '/userhr/user_collect', '/userhr/colldown_status', '/userhr/user_datastatis', '/userhr/look_resume',
#                       '/userhr/download_file', '/resume/collect_resumelist', '/userhr/user_logout',
#                       '/userhr/user_alarm']

logger = logging.getLogger('log')

# 登录拦截校验器
class LoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        uid = request.POST.get('uid')
        if uid:
            server_session = con.get('user:' + uid)
            session = cache.get('user_session:' + uid)
            try:
                cookie_session = request.COOKIES['session']
                logger.info('读取到的COOKIE参数：{}'.format(request.COOKIES))
            except:
                logger.error('无法读取COOKIES中的session信息')
                cookie_session = None

            # if not(session == cookie_session):
            #     logger.info('您的帐号已经在其他地方登录')
            #     return JsonResponse({'status': 203, 'msg': '您的帐号已经在其他地方登录', 'data': {}})

            if not server_session:
                return JsonResponse({'status': 201, 'msg': '用户未登录', 'data': {}})

            status = eval(server_session)
            logger.info('该用户{}的状态为：{}'.format(uid, status))
            if status == 0:
                return JsonResponse({'status': 409, 'msg': '帐号已冻结', 'data': {}})

            logger.info('{}用户正在操作，更新过期时间'.format(uid))
            con.expire('user:' + uid, USER_CACHE_TIME)

        # 检查用户是否属于登录用户
        # if request.path in loginRequired_list:
        #     if not server_session:
        #         logger.info('{}该用户未登录'.format(uid))
        #         return JsonResponse({'status': 201, 'msg': '用户未登录', 'data': {}})
        #     else:
        #         logger.info('{}用户正在操作，更新过期时间'.format(uid))
        #         con.expire('user:' + uid, 60 * 30)
        # else:
        # 免登录的部分列表传参带有UID信息所以需要更新用户的在线时长
        # if uid and server_session:
        #     logger.info('{}用户正在操作，更新过期时间'.format(uid))
        #     con.expire('user:' + uid, 60 * 30)

    '''
    def process_response(self,request,response):
        # 解决用户跨域访问的问题
        # logger.info('检测到用户有个跨域请求，查看对方的method-->{}'.format(request.method))

        # 复杂请求，会先发送预检请求OPTIONS
        if request.method == 'OPTIONS':
            response['Access-Control-Allow-Headers'] = 'Content-Type,X-Requested-With,X-CSRFToken'
            response['Access-Control-Allow-Methods'] = 'POST,PUT,PATCH,DELETE'
        else:
            # 简单请求
            response['Access-Control-Allow-Origin'] = '*'

        return response
    '''

    # def process_template_response(self):
    #     pass
    #
    # def process_view(self,request,callback,callback_args,callback_kwargs):
    #     pass
    #
    # def process_exception(self,request,exception):
    #     pass
