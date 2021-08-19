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
from django.db.models import Q

from userhr.models import SysMember

logger = logging.getLogger('log')


# 从SysMember表中获取用户基本信息，并设置到redis中
def search_user(uid=None,phone=None):
    # if uid:
    #     user = cache.get('user:detail_' + uid)
    #     logger.info('从缓存中获取{}用户的详情，获取到的数据为：{}'.format(uid, user))
    # else:
    #     user = cache.get('user:detail_phone_' + phone)
    #     logger.info('从缓存中获取{}用户的详情，获取到的数据为：{}'.format(phone, user))

    # if not user:
    #     logger.info('没有查询到缓存数据，从数据库中提取并永久缓存')
    user = SysMember.objects.filter(Q(id=uid) | Q(phone=phone)).first()

        # cache.set('user:detail_' + user.id, user)
        # cache.persist('user:detail_' + user.id)
        # cache.set('user:detail_phone_' + user.phone, user)
        # cache.persist('user:detail_phone_' + user.phone)

    return user