#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ResumeRecommend.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/9/1 11:12   gxrao      1.0         None
'''
import logging

from django.core.cache import cache

from ThinkJob.settings import RESUME_CACHE_TIME
from resume.models import HrResumeBase

logger = logging.getLogger('log')


# 推荐列表，可以被当做简历评分排序使用
def recommend():
    # 从redis中获取推荐列表
    redis_auth_recommend = cache.get('recommend')
    if redis_auth_recommend:
        return redis_auth_recommend

    # 从redis中获取推荐列表失败，开始重建redis缓存
    base_list_obj = HrResumeBase.objects.all().extra(
        tables=['hr_resume_auth'],
        where=['hr_resume_auth.pk_id = hr_resume_base.id'],
        select={'real_score': 'hr_resume_auth.real_score'}
    ).order_by('-real_score', '-create_time')

    logger.info('将auth匹配Base表的数量为：{}'.format(base_list_obj.count()))
    cache.set('recommend', base_list_obj, RESUME_CACHE_TIME)

    return base_list_obj
