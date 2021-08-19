#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   CollectResume.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/8/18 17:11   gxrao      1.0         None
'''
import logging

from django.db.models import Q

from commer.CacheCodeObj import CacheCode
from resume.models import HrUserResumeRelation, HrResumeBase
from system.models import SysCodes

logger = logging.getLogger('log')


# 用戶收藏
def user_collect(uid, search_criteria):
    '''
        user_collect
        :param uid 用户的uid
        :param search_criteria 用户的搜索条件
        :return resume_list 一个数据库列表对象
    '''
    # 根据用户UUID以及收藏collect标识来获取当前用户的所有搜藏简历，并返回简历id
    # user_collects = HrUserResumeRelation.objects.filter(uid=uid, type='collect').values_list('resume_id').order_by(
    #     '-create_time')
    # logger.info('查询到该用户的的搜藏数量：{}'.format(user_collects.__len__()))

    # 从redis中获取推荐列表失败，开始重建redis缓存
    # base_list_obj = HrResumeBase.objects.all().extra(
    #     tables=['hr_user_resume_relation'],
    #     where=['hr_user_resume_relation.uid="{}"'.format(uid),'hr_user_resume_relation.resume_id = hr_resume_base.id', 'hr_user_resume_relation.type="collect"'],
    #     select={'collect_time': 'hr_user_resume_relation.create_time'}
    # ).order_by('-collect_time')
    #
    # print(base_list_obj.query)

    # 判断是否查到了数据，如果没有数据证明该用户没有收藏信息
    # if not user_collects:
    #     return None

    # q2 = Q()
    q3 = Q()
    con = Q()
    if search_criteria:
        q1 = Q()  # 定义好一个Q对象来做高级搜索条件
        q1.children.append(('dtype', 'job'))  # dtype状态为job
        q1.children.append(('name__icontains', search_criteria))  # name包含用户搜索数据
        logger.info('q1的查询条件：{}'.format(q1))

        codes = CacheCode().filter(q1).all()
        logger.info('q1的查询结果为：{}'.format(codes.__len__()))
        if codes.__len__() > 0:
            for i in codes:
                q3.connector = 'OR'
                q3.children.append(('job_type', i.code))
        else:
            return None

    # q2.children.append(('id__in', user_collects))
    # q2.children.append(('status', '1'))
    con.add(q3, 'AND')
    # con.add(q2, 'AND')
    logger.info('con的查询条件为：{}'.format(con))

    # 根据返回的简历id去查询出所有简历的对应数据，并分页
    resume_list = HrResumeBase.objects.filter(status='1').filter(con).extra(
        tables=['hr_user_resume_relation'],
        where=['hr_user_resume_relation.uid="{}"'.format(uid),'hr_user_resume_relation.resume_id = hr_resume_base.id', 'hr_user_resume_relation.type="collect"'],
        select={'collect_time': 'hr_user_resume_relation.create_time'}
    ).order_by('-collect_time')

    return resume_list
