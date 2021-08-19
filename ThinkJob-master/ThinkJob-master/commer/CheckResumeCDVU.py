#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   CheckResumeCDVU.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/9/2 9:42   gxrao      1.0         None
'''
import logging

from resume.models import HrUserResumeRelation

logger = logging.getLogger('log')

def checkresume_cdvu(uid,resume_id):
    usercollect = HrUserResumeRelation.objects.filter(uid=uid, resume_id=resume_id).all()
    logger.info('{}用户要查询的这个{}简历有{}个状态了'.format(uid, resume_id, usercollect.__len__()))

    if usercollect:
        data_status = {
            'collect': False,
            'down': False,
            'view': False,
            'upload': False,
        }
        for i in usercollect:
            data_status[i.type] = True
        return data_status
    else:
        data_status = {
            'collect': False,
            'down': False,
            'view': False,
            'upload': False,
        }
        return data_status