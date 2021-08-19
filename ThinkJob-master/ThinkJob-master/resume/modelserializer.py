#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   modelserializer.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/8/12 10:29   gxrao      1.0         None
'''
import logging
import random
from datetime import datetime

from django.core.cache import cache
from rest_framework import serializers

from ThinkJob.settings import RESUME_CACHE_TIME
from commer.CacheCodeObj import CacheCode
from commer.CheckResumeAuth import check_resumeauth
from commer.CheckResumeCDVU import checkresume_cdvu
from commer.NameHidden import namehidden
from commer.RandomNum import numr
from commer.ResumeIsRead import resume_isread
from commer.SalaryHidden import salaryhidden
from commer.TimeRel import released_time
from resume.models import HrResumeBase, HrResumeAuth, HrResumeWorkprocess, HrResumeEducation
from system.models import SysUser

logger = logging.getLogger('log')


class HrResumeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = HrResumeBase
        # 以下都是显示的值
        fields = (
            'id', 'name', 'sex', 'age', 'live_address', 'native_place', 'birthday', 'phone', 'e_mail',
            'learn_certificate', 'view_url',
            'expect_salary', 'current_salary', 'job_status', 'marriage', 'politics_status', 'self_evaluation',
            'up_user_id', 'school', 'profession', 'opt_time', 'work_process')


class HrResumeWorkprocessSerializer(serializers.ModelSerializer):
    class Meta:
        model = HrResumeWorkprocess
        # 以下都是显示的值
        fields = ('company_name', 'work_start_date', 'work_end_date', 'work_job')


# 学习经历序列化功能
class ResumeEduSerializer(serializers.ModelSerializer):
    class Meta:
        model = HrResumeEducation
        # 以下都是显示的值
        fields = ('id', 'pk_id', 'school_name', 'in_school_date', 'out_school_date', 'learn_certificate', 'degree')


class BaseToWorkSerializer(serializers.ModelSerializer):
    # 新增一个需要序列化的workpro对象进去
    workpro = serializers.SerializerMethodField()
    # 新增一个需要序列化的collsta对象进去
    collsta = serializers.SerializerMethodField()
    # 新增一个学习经历的序列化对象进去
    education = serializers.SerializerMethodField()
    # 对job_type进行code码转换
    job_type = serializers.SerializerMethodField()
    # 对learn_certificate进行code码转换
    learn_certificate = serializers.SerializerMethodField()
    # 转换系统时间
    opt_time = serializers.SerializerMethodField()
    # 学校性质code码转换
    school_nature = serializers.SerializerMethodField()
    # 处理姓名隐私
    name = serializers.SerializerMethodField()
    # 薪资区间化隐私处理
    expect_salary = serializers.SerializerMethodField()
    # 该简历是否查看
    isread = serializers.SerializerMethodField()
    # 修复job_status状态为空的时候显示“”的问题
    job_status = serializers.SerializerMethodField()
    # 修复live_address状态为空的时候显示的问题
    live_address = serializers.SerializerMethodField()

    class Meta:
        model = HrResumeBase
        # 以下都是显示的值，在值的末尾添加workpro对象
        fields = (
            'id', 'name', 'sex', 'age', 'live_address', 'native_place', 'birthday',
            'learn_certificate', 'job_type', 'school_nature',
            'expect_salary', 'current_salary', 'job_status', 'marriage', 'politics_status',
            'up_user_id', 'school', 'profession', 'opt_time', 'work_process', 'workpro', 'education', 'collsta'
            , 'isread', 'integral')

    def get_live_address(self, obj):
        live_address = obj.live_address
        if live_address == '' or live_address == None:
            return '未知'
        else:
            return live_address

    # 修复job_status状态为空的时候显示“”的问题
    def get_job_status(self, obj):
        job_status = obj.job_status
        if job_status == '' or job_status == None:
            return '离职'
        return job_status

    # 简历的阅读状态
    def get_isread(self, obj):
        resume_id = obj.id
        uid = self.context['uid']
        if not uid:
            return False
        return resume_isread(uid, resume_id)

    # 薪资区间化隐私处理
    def get_expect_salary(self, obj):
        expect_salary = obj.expect_salary
        if not expect_salary:
            # 如果没有薪资的话从列表中随机抽取一个薪资
            sal_list = [10000, 11000, 12000, 13000, 14000, 15000, 16000]
            return salaryhidden(random.choice(sal_list))
        return salaryhidden(expect_salary)

    # 将name进行隐私化处理
    def get_name(self, obj):
        name = obj.name
        if not name:
            return ''
        return namehidden(name)

    # school_nature码转换
    def get_school_nature(self, obj):
        school_nature_code = obj.school_nature
        if school_nature_code:
            code_obj = CacheCode().filter(dtype='education_way', code=school_nature_code).first()
            return code_obj.name
        return ''

    # opt_time时间转换
    def get_opt_time(self, obj):
        opt_time = obj.opt_time
        if opt_time:
            date_obj = datetime.strptime(opt_time, '%Y-%m-%d %H:%M:%S')
            return released_time(date_obj)
        return '未知'

    # get_learn_certificate进行code码转换
    def get_learn_certificate(self, obj):
        learn_certificate_code = obj.learn_certificate
        if learn_certificate_code:
            code_name = CacheCode().filter(dtype='education', code=learn_certificate_code).first()
            if not code_name:
                return learn_certificate_code
            return code_name.name
        return '未知'

    # job_type进行code码转换
    def get_job_type(self, obj):
        job_type_code = obj.job_type
        if job_type_code:
            code_name = CacheCode().filter(dtype='job', code=job_type_code).first()
            if not code_name:
                return '未知'
            return code_name.name
        return '未知'

    # 创建一个workpro对象数据的获取方式，由于会出现多表联查的情况，所以需要将查询到的数据载入redis中，防止查询过慢
    def get_workpro(self, obj):
        user = obj

        user_workprolist = cache.get('serializer:workpro:' + str(user))
        logger.debug('从redis中获取的{}数据为：{}'.format('serializer:workpro:' + str(user), user_workprolist))

        if not user_workprolist:
            user_workprolist = HrResumeWorkprocess.objects.filter(pk_id=user).all().order_by('-work_start_date')
            if not user_workprolist:
                # 查到了数据在进行设置缓存，否则不设置缓存
                cache.set('serializer:workpro:' + str(user), user_workprolist, RESUME_CACHE_TIME)
        user_workprolist_s = HrResumeWorkprocessSerializer(user_workprolist, many=True)

        # 创建一个空列表去装载数据
        list_detail = []

        for i in user_workprolist_s.data:
            resume_use = {}
            for k, v in i.items():
                resume_use[k] = '' if v is None else v
            list_detail.append(resume_use)

        return list_detail

    # 创建一个collsta对象数据的获取方式
    def get_collsta(self, obj):
        resume_id = obj
        # 使用context参数来从前端获取传递的uid数据
        uid = self.context['uid']
        if not uid:
            data_status = {
                'collect': False,
                'down': False,
                'view': False,
                'upload': False,
            }
            return data_status
        return checkresume_cdvu(uid, resume_id)

    # 创建一个education对象数据的获取方式，用来展现学历信息
    def get_education(self, obj):
        user = obj
        user_listobj = cache.get('serializer:edu:' + str(user))
        logger.debug('从redis中获取的{}数据为：{}'.format('serializer:edu:' + str(user), user_listobj))
        if not user_listobj:
            user_listobj = HrResumeEducation.objects.filter(pk_id=str(user)).all().order_by('-out_school_date')
            if not user_listobj:
                cache.set('serializer:edu:' + str(user), user_listobj, RESUME_CACHE_TIME)

        edu_list = ResumeEduSerializer(user_listobj, many=True).data

        return edu_list


class HrResumeAuthSerializer(serializers.ModelSerializer):
    create_time = serializers.SerializerMethodField()
    create_psn = serializers.SerializerMethodField()
    job_ranking = serializers.SerializerMethodField()
    hands_on = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = HrResumeAuth
        # 以下都是显示的值
        fields = ('education_info', 'company_info', 'is_job', 'language_level', 'address', 'apply_job', 'create_time',
                  'create_psn', 'real_score', 'hands_on', 'job_ranking', 'star_level')

    def get_address(self, obj):
        address = obj.address
        if not address:
            return '未知'
        else:
            return address

    def get_hands_on(self, obj):
        hands_on = obj.hands_on
        if '0' in hands_on:
            return '平均换工作率 未知'
        else:
            return hands_on

    def get_job_ranking(self, obj):
        job_ranking = obj.job_ranking
        if job_ranking:
            return job_ranking
        return numr()

    def get_create_time(self, obj):
        create_time = obj.create_time
        if create_time:
            date_obj = datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')
            return released_time(date_obj)
        return '未知'

    def get_create_psn(self, obj):
        sys_user = obj.create_psn
        sys_user_obj = SysUser.objects.filter(username=sys_user).first()
        if not sys_user_obj:
            return sys_user
        return sys_user_obj.name


class ResumeDetailSerializer(serializers.ModelSerializer):
    # 新增一个需要序列化的collsta对象进去
    collsta = serializers.SerializerMethodField()
    # 新增一核验信息数据进去
    resumeauth = serializers.SerializerMethodField()
    # 对job_type进行code码转换
    job_type = serializers.SerializerMethodField()
    # 对learn_certificate进行code码转换
    learn_certificate = serializers.SerializerMethodField()
    # 对phone进行隐私隐藏
    phone = serializers.SerializerMethodField()
    # 对Email进行隐私隐藏
    e_mail = serializers.SerializerMethodField()
    # 对用户的name进行隐藏
    name = serializers.SerializerMethodField()
    # 将金额进行模糊显示
    expect_salary = serializers.SerializerMethodField()
    # 将地址转成数组
    img_url = serializers.SerializerMethodField()
    # 根据参数隐藏view_url
    view_url = serializers.SerializerMethodField()
    # 修复job_status状态为空的时候显示“”的问题
    job_status = serializers.SerializerMethodField()

    class Meta:
        model = HrResumeBase
        # 以下都是显示的值
        fields = (
            'id', 'name', 'sex', 'live_address', 'phone', 'e_mail', 'learn_certificate', 'job_type', 'expect_salary',
            'current_salary',
            'job_status', 'school', 'profession', 'work_process', 'collsta', 'resumeauth',
            'view_url', 'integral', 'sel_type', 'img_url', 'memo')

    # 修复job_status状态为空的时候显示“”的问题
    def get_job_status(self, obj):
        return BaseToWorkSerializer.get_job_status(self, obj)

    # 根据参数隐藏view_url
    def get_view_url(self, obj):
        sel_type = obj.sel_type
        if not sel_type:
            return ''
        elif sel_type == 'image':
            return ''
        else:
            return obj.view_url

    # 将图片地址转成数组
    def get_img_url(self, obj):
        sel_type = obj.sel_type
        img_url = obj.img_url
        if not sel_type:
            return ''
        elif sel_type == 'image':
            img_url = img_url.split(';')
        return img_url

    # 薪资区间化隐私处理
    def get_expect_salary(self, obj):
        return BaseToWorkSerializer.get_expect_salary(self, obj)

    # 对用户的name进行隐藏
    def get_name(self, obj):
        resume_id = obj.id
        name = obj.name
        uid = self.context['uid']
        if not name:
            return '--'
        if not uid:
            return namehidden(name)
        else:
            cdvu_obj = checkresume_cdvu(uid, resume_id)
            if cdvu_obj['down'] or cdvu_obj['view']:
                return name
            else:
                return namehidden(name)

    def get_opt_time(self, obj):
        return BaseToWorkSerializer.get_opt_time(self, obj)

    def get_learn_certificate(self, obj):
        return BaseToWorkSerializer.get_learn_certificate(self, obj)

    def get_job_type(self, obj):
        return BaseToWorkSerializer.get_job_type(self, obj)

    def get_collsta(self, obj):
        return BaseToWorkSerializer.get_collsta(self, obj)

    def get_phone(self, obj):
        phone = obj.phone
        resume_id = obj.id
        uid = self.context['uid']
        if not phone:
            return '--'
        if not uid:
            return phone[:3] + '****' + phone[7:]
        else:
            cdvu_obj = checkresume_cdvu(uid, resume_id)
            if cdvu_obj['down'] or cdvu_obj['view']:
                return phone
            else:
                return phone[:3] + '****' + phone[7:]

    def get_e_mail(self, obj):
        e_mail = obj.e_mail
        resume_id = obj.id
        uid = self.context['uid']
        if not e_mail:
            return '--'
        if not uid:
            return e_mail[:3] + "****" + e_mail[7:]
        else:
            cdvu_obj = checkresume_cdvu(uid, resume_id)
            if cdvu_obj['down'] or cdvu_obj['view']:
                return e_mail
            else:
                return e_mail[:3] + '****' + e_mail[7:]

    def get_resumeauth(self, obj):
        resume_id = str(obj.id)
        resume_auth_obj = check_resumeauth(resume_id)
        resume_auth_list = HrResumeAuthSerializer(resume_auth_obj)

        # 下面的代码主要是为了去除值为None的结果
        list = {}
        for k, v in resume_auth_list.data.items():
            list[k] = '' if v == None else v
        return list
