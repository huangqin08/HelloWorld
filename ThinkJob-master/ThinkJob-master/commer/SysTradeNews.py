#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   SysTradeNews.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/9/14 11:57   gxrao      1.0         None
'''
import logging

from django.core.cache import cache

from system.models import SysTradenews

logger = logging.getLogger('log')

def systradenews():
    tradenews_obj = cache.get('systradenews')
    if not tradenews_obj:
        tradenews_obj = SysTradenews.objects.all()
        cache.set('systradenews',tradenews_obj,None)
    return tradenews_obj
