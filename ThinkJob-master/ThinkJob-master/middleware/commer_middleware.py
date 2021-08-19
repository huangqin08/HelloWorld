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

from django.utils.deprecation import MiddlewareMixin

from commer.CheckIP import checkip

logger = logging.getLogger('log')


# 公共拦截器，做一些数据记录使用
class CommerMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.info('用户提交POST的数据：{}'.format(request.POST.get))
        logger.info('用户提交GET的数据：{}'.format(request.POST.get))
        # 为了防止暴力请求，这里需要获取一下用户的请求IP
        checkip(request)
        # 用户的请求路径
        logger.info('HttpRequest.path：{}'.format(request.path))
