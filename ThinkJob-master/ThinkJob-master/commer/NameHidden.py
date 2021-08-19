#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   NameHidden.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/9/2 10:46   gxrao      1.0         None
'''
import logging

logger = logging.getLogger('log')

def namehidden(name):
    logger.debug('需要隐私化的名字为：{}'.format(name))
    if name.__len__() == 2:
        return name[:1] +'*'
    if name.__len__() > 2:
        return name[:1] +('*'*(name.__len__()-2))+name[-1:]
