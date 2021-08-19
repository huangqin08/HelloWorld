#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   CacheCodeObj.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/8/25 14:57   gxrao      1.0         None
'''
import logging

from django.core.cache import cache

from system.models import SysCodes

logger = logging.getLogger('log')


# 开始向redis里存一份code对象
def CacheCode():
    # 从redis中获取code对象
    code_obj = cache.get('code_obj')
    logger.debug('从redis中获取到的code_obj对象为：{}'.format(code_obj))
    if not code_obj:
        logger.info('没有从redis中获取到code对象，重新去数据库中拿一份')
        try:
            code_obj = SysCodes.objects.filter(status='1')
            cache.set('code_obj', code_obj)
            cache.persist('code_obj')
        except Exception as e:
            logger.error('code码这出现错误信息：{}'.format(e))
    return code_obj
