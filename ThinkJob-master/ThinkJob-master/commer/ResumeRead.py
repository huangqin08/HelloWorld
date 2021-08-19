#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ResumeRead.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/9/1 10:47   gxrao      1.0         None
'''
import logging
import uuid
from datetime import datetime

from resume.models import HrUserResumeRead
logger = logging.getLogger('log')

def resume_read(request):
    resume_id = request.POST.get('resume_id')
    uid = request.POST.get('uid')
    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 创建时间

    # 有用户查看这个简历的时候记录一条数据
    resume_read_obj = HrUserResumeRead()
    resume_read_obj.id = str(uuid.uuid1().hex)
    resume_read_obj.uid = uid if uid else 'NoLogin'
    resume_read_obj.resume_id = resume_id
    resume_read_obj.create_time = create_time
    resume_read_obj.memo = '此简历{}在这时间{}被{}用户查看了'.format(resume_id, create_time, (uid if uid else 'NoLogin'))
    resume_read_obj.save()

    logger.info('此简历{}在这时间{}被{}用户查看了'.format(resume_id, create_time, (uid if uid else 'NoLogin')))