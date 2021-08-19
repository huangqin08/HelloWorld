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

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('log')


# 公共拦截器，做校验必传参数丢失校验
class ParamCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        status = True

        if request.path in '/api2/userhr/user_login':
            phone = request.POST.get('phone')
            user_pwd = request.POST.get('user_pwd')
            status = all([phone, user_pwd])
        elif request.path in '/api2/userhr/register':
            phone = request.POST.get('phone')
            user_pwd = request.POST.get('user_pwd')
            company_name = request.POST.get('company_name')
            status = all([phone, user_pwd, company_name])
        elif request.path in '/api2/userhr/checkphone':
            phone = request.GET.get('phone')
            status = all([phone])
        elif request.path in ['/api2/userhr/editor_user', '/api2/userhr/detail_user', '/api2/userhr/user_datastatis',
                              '/api2/userhr/user_logout']:
            uid = request.POST.get('uid')
            status = all([uid])
        elif request.path in ['/api2/userhr/checkpassword']:
            uid = request.POST.get('uid')
            user_pwd_new = request.POST.get('user_pwd_new')
            user_pwd_old = request.POST.get('user_pwd_old')
            status = all([uid, user_pwd_new, user_pwd_old])
        elif request.path in ['/api2/userhr/forget_pwd']:
            phone = request.POST.get('phone')
            user_pwd_new = request.POST.get('user_pwd_new')
            message_code = request.POST.get('message_code')
            status = all([phone, user_pwd_new, message_code])
        elif request.path in '/api2/userhr/resume_update':
            uid = request.POST.get('uid')
            status = all([uid])
        elif request.path in ['/api2/userhr/user_collect', '/api2/userhr/look_resume', '/api2/userhr/download_file',
                              '/api2/userhr/colldown_status', '/api2/userhr/user_alarm']:
            uid = request.POST.get('uid')
            resume_id = request.POST.get('resume_id')
            status = all([uid, resume_id])
        elif request.path in ['/api2/userhr/message_login']:
            phone = request.POST.get('phone')
            message_code = request.POST.get('message_code')
            status = all([phone, message_code])
        elif request.path in ['/api2/resume/resume_list_all', '/api2/resume/resume_search', '/api2/resume/job_search',
                              '/api2/resume/resume_recommend', '/api2/resume/new_job_search',
                              '/api2/resume/new_resume_search', '/api2/resume/new_resume_list_all']:
            page = request.POST.get('page')
            page_size = request.POST.get('page_size')
            status = all([page, page_size])
        elif request.path in ['/api2/resume/check_resume_auth', '/api2/resume/resume_detail']:
            resume_id = request.POST.get('resume_id')
            status = all([resume_id])
        elif request.path in ['/api2/resume/collect_resumelist', '/api2/userhr/userupdate_list']:
            uid = request.POST.get('uid')
            page = request.POST.get('page')
            page_size = request.POST.get('page_size')
            status = all([uid, page, page_size])
        elif request.path in '/api2/system/message_code':
            phone = request.POST.get('phone')
            status = all([phone])
        elif request.path in '/api2/userhr/user_alarm':
            uid = request.POST.get('uid')
            resume_id = request.POST.get('resume_id')
            chk_phone = request.POST.get('chk_phone')
            chk_work = request.POST.get('chk_work')
            status = all([uid, resume_id, chk_phone, chk_work])

        if not status:
            logger.info('发现用户必传参数丢失')
            return JsonResponse({'status': 201, 'msg': '必传参数丢失'})
