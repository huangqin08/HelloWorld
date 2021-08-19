#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   TodayResumeDownloads.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/9/27 17:12   gxrao      1.0         None
'''

import logging
from datetime import datetime

from django.db.models import Q

from ThinkJob.settings import con
from resume.models import HrUserResumeRelation

logger = logging.getLogger('log')


def today_resume_downloads(uid, state='get', u_num=1):
    time = datetime.now().strftime('%Y-%m-%d')
    num = con.get('{}:{}'.format(time, uid))
    if state == 'get' and num:
        return eval(num)
    elif state == 'get' and not num:
        num = HrUserResumeRelation.objects.filter(uid=uid, create_time__contains=time).filter(
            Q(type='view') | Q(type='down')).count()
        con.set('{}:{}'.format(time, uid), num, 60 * 60 * 8)
        return int(num)
    elif state == 'set' and num:
        num = eval(num) + u_num
        con.set('{}:{}'.format(time, uid), num, 60 * 60 * 8)
        return int(num)
    else:
        num = HrUserResumeRelation.objects.filter(uid=uid, create_time__contains=time).filter(
            Q(type='view') | Q(type='down')).count()
        num = num + u_num
        con.set('{}:{}'.format(time, uid), num, 60 * 60 * 8)
        return int(num)