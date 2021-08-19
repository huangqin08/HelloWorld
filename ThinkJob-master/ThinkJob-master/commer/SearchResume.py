# -*- encoding: utf-8 -*-
'''
@File    :   SearchResume.py
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/8/18 14:34   gxrao      1.0         None
'''
import logging

from django.core.cache import cache
from django.db.models import Q

from ThinkJob.settings import RESUME_CACHE_TIME
from commer.CacheCodeObj import CacheCode

from resume.models import HrResumeBase
from system.models import SysCodes

logger = logging.getLogger('log')


# 从HrResumeBase表中获取所有简历信息，并设置到redis中
def search_resume_list_all(status=1):
    '''
        search_resume_list_all
        :param status 有效的简历1  无效的简历0
        :return resume_list 一个数据库列表对象
    '''
    resume_list = cache.get('search:resume_list_all')
    logger.info('获取缓存search:resume_list_all数据为：{}'.format(resume_list))
    if not resume_list:
        logger.info('缓存中没有search:resume_list_all，正在设置')
        resume_list = HrResumeBase.objects.filter(status=status).all().order_by('-opt_time')
        if resume_list:
            cache.set('search:resume_list_all', resume_list, RESUME_CACHE_TIME)  # 将搜索数据设置到redis中，并设置1小时有效
            return resume_list
        else:
            return None
    else:
        return resume_list


# 从HrResumeBase表中按照搜索条件获取简历信息，并设置到redis中
def search_resume_condition_query(**kwargs):
    '''
        search_resume_condition_query
        :param job 职位
        :param education 学历
        :param work_process 工作经验
        :param expectsalary 期望薪资
        :paramisjob 是否在职
        :parameducation_way 学校性质
        :paramschool_type 学校等级
        :payrange_start 薪资范围搜索，起始范围
        :payrange_end 薪资范围搜索，结束范围
        :return resume_list 一个数据库列表对象
    '''

    # 将调用方法的参数进行下输出，好记录错误
    for k, v in kwargs.items():
        logger.info('search_resume_condition_query-->{}:{}'.format(k, v))

    resume_list = cache.get(
        'search:uid_{}:resume_search:job_{}:education_{}:workprocess_{}:expectsalary_{}:isjob_{}:educationway_{}:schooltype_{}:'
        'payrangestart_{}:payrangeend_{}'.format(kwargs['uid'],
                                                 kwargs['job'], kwargs['education'], kwargs['work_process'],
                                                 kwargs['expectsalary'], kwargs['isjob'],
                                                 kwargs['education_way'], kwargs['school_type'],
                                                 kwargs['payrange_start'], kwargs['payrange_end']))
    logger.info(
        '缓存中search:uid_{}:resume_search:job_{}:education_{}:workprocess_{}:expectsalary_{}:isjob_{}:educationway_{}:'
        'schooltype_{}:payrangestart_{}:payrangeend_{}'.format(kwargs['uid'],
                                                               kwargs['job'], kwargs['education'],
                                                               kwargs['work_process'], kwargs['expectsalary'],
                                                               kwargs['isjob'],
                                                               kwargs['education_way'], kwargs['school_type'],
                                                               kwargs['payrange_start'], kwargs['payrange_end'],
                                                               resume_list))

    if not resume_list:
        logger.info('没有找到缓存数据，开始数据库条件搜索')

        q1 = Q()  # 定义好一个Q对象来做高级搜索条件
        q2 = Q()
        con = Q()
        q1.children.append(('status', '1'))  # 简历状态为1是活动简历

        # 判断用户是否带了uid
        if kwargs['uid']:
            q2.children.append(('up_user_id', kwargs['uid']))

        # 判断用户是否带了job的搜索条件
        if kwargs['job']:
            q1.children.append(('job_type', kwargs['job']))

        # 判断用户是否带了education的搜索条件
        if kwargs['education']:
            q1.children.append(('learn_certificate', kwargs['education']))

        # 判断用户是否带了isjob的code码
        if kwargs['isjob']:
            name = CacheCode().filter(code=kwargs['isjob'], dtype='isjob').values_list('name').first()
            q1.children.append(('job_status', name[0]))

        # 判断用户是否带了education_way的code码
        if kwargs['education_way']:
            q1.children.append(('school_nature', kwargs['education_way']))

        # 判断用户是否带了school_type的code码
        if kwargs['school_type']:
            q1.children.append(('school_level', kwargs['school_type']))

        # 判断用户是否带了workprocess的搜索条件，如果有workprocess的搜索条件，对一些code码进行处理
        if kwargs['work_process']:
            name = CacheCode().filter(code=kwargs['work_process'], dtype='workprocess').values_list('name').first()
            logger.info('打印当前workprocess的code码信息--------->{}'.format(name))
            if '应届生' in name:
                q1.children.append(('work_process', '0'))
            elif '1年以内' in name:
                q1.children.append(('work_process__gt', '0'))
                q1.children.append(('work_process__lte', '1'))
            elif '1-3年' in name:
                q1.children.append(('work_process__gte', '1'))
                q1.children.append(('work_process__lt', '3'))
            elif '3-5年' in name:
                q1.children.append(('work_process__gte', '3'))
                q1.children.append(('work_process__lt', '5'))
            elif '5年及以上' in name:
                q1.children.append(('work_process__gte', '5'))

        # 判断用户是否带了expectsalary的搜索条件，如果有expectsalary的搜索条件，对一些code码进行处理
        if kwargs['expectsalary']:
            name = CacheCode().filter(code=kwargs['expectsalary'], dtype='expectsalary').values_list('name').first()
            logger.info('打印当前expectsalary的code码信息--------->{}'.format(name))
            if '5k-10k' in name:
                q1.children.append(('expect_salary__gte', '5000'))
                q1.children.append(('expect_salary__lt', '10000'))
            elif '10k-15k' in name:
                q1.children.append(('expect_salary__gte', '10000'))
                q1.children.append(('expect_salary__lt', '15000'))
            elif '15k-20k' in name:
                q1.children.append(('expect_salary__gte', '15000'))
                q1.children.append(('expect_salary__lt', '20000'))
            elif '20k-25k' in name:
                q1.children.append(('expect_salary__gte', '20000'))
                q1.children.append(('expect_salary__lt', '25000'))
            elif '25k-30k' in name:
                q1.children.append(('expect_salary__gte', '25000'))
                q1.children.append(('expect_salary__lt', '30000'))
            elif '30k-40k' in name:
                q1.children.append(('expect_salary__gte', '30000'))
                q1.children.append(('expect_salary__lt', '40000'))
            elif '40k-50k' in name:
                q1.children.append(('expect_salary__gte', '40000'))
                q1.children.append(('expect_salary__lt', '50000'))
        else:
            if kwargs['payrange_start'] and kwargs['payrange_end']:
                q1.children.append(('expect_salary__gte', kwargs['payrange_start']))
                q1.children.append(('expect_salary__lte', kwargs['payrange_end']))
            elif not (kwargs['payrange_start']) and kwargs['payrange_end']:
                q1.children.append(('expect_salary__gte', 0))
                q1.children.append(('expect_salary__lte', kwargs['payrange_end']))
            elif kwargs['payrange_start'] and not (kwargs['payrange_end']):
                q1.children.append(('expect_salary__gte', kwargs['payrange_start']))
                q1.children.append(('expect_salary__lte', 99999999))

        con.add(q1, 'AND')
        con.add(q2, 'AND NOT')
        logger.info('打印搜索条件：{}'.format(con))

        resume_list = HrResumeBase.objects.filter(con).order_by('-opt_time')
        # print(resume_list.query)
        # logging.info('需要检查的sql语句为：{}'.format(resume_list.query))

        if resume_list:
            logger.info('数据库值搜索成功，共找到{}条数据，并将数据设置到redis中'.format(resume_list.__len__()))
            cache.set(
                'search:uid_{}:resume_search:job_{}:education_{}:workprocess_{}:expectsalary_{}:isjob_{}:educationway_{}:schooltype_{}:'
                'payrangestart_{}:payrangeend_{}'.format(kwargs['uid'],
                                                         kwargs['job'], kwargs['education'], kwargs['work_process'],
                                                         kwargs['expectsalary'], kwargs['isjob'],
                                                         kwargs['education_way'], kwargs['school_type'],
                                                         kwargs['payrange_start'],
                                                         kwargs['payrange_end']), resume_list, RESUME_CACHE_TIME)
            return resume_list
        else:
            return None
    else:
        return resume_list


# 从HrResumeBase表中按照职位条件获取简历信息，并设置到redis中
def search_resume_job(uid, search_job):
    '''
        search_resume_job
        :param search_job 职位
        :return resume_list 一个数据库列表对象
    '''

    # 首先根据用户的查询条件去缓存中获取历史搜索数据
    resume_list = cache.get('search:uid_{}:job_search:{}'.format(uid, search_job))
    logger.info('缓存中search:uid_{}:job_search:{}的数据为：{}'.format(uid, search_job, resume_list))
    if not resume_list:
        logger.info('缓存中没有找到search_job_search_{}的数据，正在按照搜索条件进行设置'.format(search_job))
        q1 = Q()  # 定义好一个Q对象来做高级搜索条件
        q2 = Q()  # 定义一个code码的查询对象
        q1.children.append(('dtype', 'job'))  # dtype状态为job
        q1.children.append(('name__icontains', search_job))  # name包含用户搜索数据
        logger.info('code的查询条件：{}'.format(q1))
        codes = CacheCode().filter(q1).all()
        if not codes:
            logger.info('没有符合要求的code码，错误的搜索条件，直接返回无数据，不设置redis')
            return None

        for i in codes:
            q2.connector = 'OR'
            q2.children.append(('job_type', i.code))
        logger.info('code的查询码：{}'.format(q2))
        # 根据返回的简历id去查询出所有简历的对应数据，并分页
        resume_list = HrResumeBase.objects.filter(status='1').filter(~Q(up_user_id=uid)).filter(q2).all().order_by('-opt_time')
        # print(resume_list.query)
        if not resume_list:
            logger.info('按照con的搜索条件没有查询到符合要求的数据，设置redis缓存失败')
            # 准备给前端返回的数据信息
            return None
        else:
            logger.info('缓存数据设置中')
            cache.set('search:job_search:{}'.format(search_job), resume_list,
                      RESUME_CACHE_TIME)  # 设置缓存数据，并将缓存数据设置1小时
            return resume_list

    else:
        return resume_list
