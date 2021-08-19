#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ResumeIsRead.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/9/2 11:52   gxrao      1.0         None
'''
import logging

from django.core.cache import cache

from resume.models import HrUserResumeRead

logger = logging.getLogger('log')

def resume_isread(uid, resume_id):
    use_isread = cache.get('isread:' + uid + ':' + resume_id)
    if not use_isread:
        list_obj = HrUserResumeRead.objects.filter(uid=uid, resume_id=resume_id).count()
        if list_obj > 0:
            cache.set('isread:' + uid + ':' + resume_id, True)
            cache.persist('isread:' + uid + ':' + resume_id)
            return True
        else:
            return False
    return use_isread
