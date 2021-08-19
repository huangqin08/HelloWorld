#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ResumeEvaluating.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/9/14 16:19   gxrao      1.0         None
'''
import logging

from django.core.cache import cache

from resume.models import HrResumeEvaluating

logger = logging.getLogger('log')

def resumeEvaluating():
    resumeEvaluating_obj = cache.get('resumeEvaluating')
    if not resumeEvaluating_obj:
        resumeEvaluating_obj = HrResumeEvaluating.objects.all()
        cache.set('resumeEvaluating', resumeEvaluating_obj, None)
    return resumeEvaluating_obj
