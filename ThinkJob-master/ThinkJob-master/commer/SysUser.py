#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   SysMemberUser.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/8/19 10:24   gxrao      1.0         None
'''
import logging

from django.core.cache import cache

from system.models import SysUser

logger = logging.getLogger('log')


# 从SysMember表中获取用户基本信息，并设置到redis中
def search_sysuser(user_id=None):
    user = cache.get('sysuser:' + user_id)
    logger.info('从缓存中获取后台{}用户，获取到的id为：{}'.format(user_id, user))

    if not user:
        logger.info('没有查询到缓存数据，从数据库中提取并永久缓存')
        user = SysUser.objects.filter(user_id=user_id).first()
        cache.set('sysuser:' + user_id, user)
        cache.persist('sysuser:' + user_id)

    return user
