#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   SalaryHidden.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/9/2 11:08   gxrao      1.0         None
'''
import logging

from commer.CacheCodeObj import CacheCode

logger = logging.getLogger('log')


def salaryhidden(salary):
    logger.debug('需要隐私化的薪资为：{}'.format(salary))
    expectsalary = CacheCode().filter(dtype='expectsalary').all()
    for i in expectsalary:
        if int(i.key_name.split('-')[0]) <= salary and int(i.key_name.split('-')[1]) >= salary:
            return i.name
    return '50k以上'
