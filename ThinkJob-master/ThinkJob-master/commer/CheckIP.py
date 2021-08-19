#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   CheckIP.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/8/20 15:46   gxrao      1.0         None
'''
import logging

logger = logging.getLogger('log')

def checkip(request):
    # 为了防止暴力请求，这里需要获取一下用户的请求IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
        logger.info('该请求的真实IP为：{}'.format(ip))
    else:
        ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
        logger.info('该请求的代理IP为：{}'.format(ip))
    return ip