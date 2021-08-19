#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   CheckResumeAuth.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/8/18 16:57   gxrao      1.0         None
'''
import logging

from django.core.cache import cache

from ThinkJob.settings import RESUME_CACHE_TIME
from resume.models import HrResumeAuth

logger = logging.getLogger('log')

# 将简历核验信息添加到缓存中
def check_resumeauth(resume_id):
    resume_auth = cache.get('auth:'+resume_id)
    logger.info('从缓存中获取的{}简历核验信息为：{}'.format(resume_id,resume_auth))

    if resume_auth:
        return resume_auth

    resume_auth = HrResumeAuth.objects.filter(pk_id=resume_id).first()
    logger.info('正在将{}简历核验信息添加到Redis中'.format(resume_id))
    cache.set('auth:' + resume_id,resume_auth,RESUME_CACHE_TIME)
    return resume_auth