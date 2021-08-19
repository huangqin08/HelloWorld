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

from rest_framework import serializers
from backstage_ment.models import HrTempEducation, HrTempWorkprocess
from commer.CacheCodeObj import CacheCode
from commer.SysMemberUser import search_user
from commer.SysUser import search_sysuser
from resume.models import HrResumeBase, HrTempBase, HrUserResumeRelation, HrResumeWorkprocess, HrResumeEducation
from system.models import SysCodes

logger = logging.getLogger('log')

# 创建HrResumeBase数据序列化，用于快速保存数据
class SaveDataHrResumeBase(serializers.ModelSerializer):
    class Meta:
        model = HrResumeBase
        fields = ('name','sex','age','live_address','native_place','birthday','phone','work_process'
                      ,'e_mail','learn_certificate','expect_salary','current_salary','job_status','marriage','politics_status'
                      ,'self_evaluation','job_type','school','profession')

# 创建HrTempBase数据序列化，用于快速保存数据
class SaveDataHrTempBase(serializers.ModelSerializer):
    class Meta:
        model = HrTempBase
        fields = ('name','sex','age','live_address','native_place','birthday','phone','work_process'
                      ,'e_mail','learn_certificate','expect_salary','current_salary','job_status','marriage','politics_status'
                      ,'self_evaluation','job_type','school','profession')


# Base表数据模型化
class HrResumeBaseSerializer(serializers.ModelSerializer):
    # 职位名称
    jobtype = serializers.SerializerMethodField()
    # 获取核验人的名称信息，通过核验人的关联id进行获取
    optuserid = serializers.SerializerMethodField()
    # 获取上传人的公司名称，通过up_user_id关联获取
    upuserid = serializers.SerializerMethodField()
    # 下载量
    downloadnum = serializers.SerializerMethodField()
    # 学历code码转换
    learncertificate = serializers.SerializerMethodField()

    class Meta:
        model = HrResumeBase
        # 以下都是显示的值
        fields = (
            'id', 'jobtype', 'phone', 'name', 'optuserid', 'work_process', 'learncertificate', 'upuserid', 'job_status',
            'update_time', 'opt_time', 'downloadnum', 'show_url')

    def get_jobtype(self, obj):
        job_type_code = obj.job_type
        if job_type_code:
            code_name = CacheCode().filter(dtype='job', code=job_type_code).first()
            if not code_name:
                return '未知'
            return code_name.name
        return '未知'

    # 获取管理系统的用户名称，用于核验人
    def get_optuserid(self, obj):
        optuserid = obj.opt_user_id
        if optuserid:
            sysuser_id = search_sysuser(user_id=str(optuserid))
            if not sysuser_id:
                return ''
            return sysuser_id.name
        return ''

    # 获取上传人的公司名称
    def get_upuserid(self, obj):
        upuserid = obj.up_user_id
        if upuserid:
            userid = search_user(uid=upuserid)
            if not userid:
                return ''
            return userid.company_name
        return ''

    # 下载量
    def get_downloadnum(self, obj):
        resume_id = obj
        downloadnum = HrUserResumeRelation.objects.filter(resume_id=resume_id, type='down').count()
        return downloadnum

    # 学历code码转换
    def get_learncertificate(self, obj):
        education_code = obj.learn_certificate
        if education_code:
            code_name = CacheCode().filter(dtype='education', code=education_code).first()
            if not code_name:
                return '未知'
            return code_name.name
        return '未知'


# 工作经历序列化功能
class ResumeWorkproSerializer(serializers.ModelSerializer):
    class Meta:
        model = HrResumeWorkprocess
        # 以下都是显示的值
        fields = (
            'id', 'pk_id', 'company_name', 'work_start_date', 'work_end_date', 'work_nature', 'work_job',
            'work_content')

# 工作经历临时表序列化功能
class TempWorkproSerializer(serializers.ModelSerializer):
    class Meta:
        model = HrTempWorkprocess
        # 以下都是显示的值
        fields = (
            'id', 'pk_id', 'company_name', 'work_start_date', 'work_end_date', 'work_nature', 'work_job',
            'work_content')


# 学习经历序列化功能
class ResumeEduSerializer(serializers.ModelSerializer):
    class Meta:
        model = HrResumeEducation
        # 以下都是显示的值
        fields = ('id', 'pk_id', 'school_name', 'in_school_date', 'out_school_date', 'learn_certificate', 'degree')

# 学习经历临时表序列化功能
class TempEduSerializer(serializers.ModelSerializer):
    class Meta:
        model = HrTempEducation
        # 以下都是显示的值
        fields = ('id', 'pk_id', 'school_name', 'in_school_date', 'out_school_date', 'learn_certificate', 'degree')


# 读取简历的所有涉及信息并序列化展现
class ReadResumeBaseSerializer(serializers.ModelSerializer):
    # 添加一个工作经历的字段进行序列化展示
    workpro = serializers.SerializerMethodField()
    # 添加一个学习经历的字段进行序列化展示
    education = serializers.SerializerMethodField()

    class Meta:
        model = HrResumeBase
        # 以下都是显示的值
        fields = (
            'id', 'name', 'sex', 'age', 'live_address', 'native_place', 'birthday', 'phone', 'work_process', 'e_mail',
            'learn_certificate', 'expect_salary', 'current_salary', 'job_status', 'marriage', 'politics_status',
            'self_evaluation', 'job_type', 'school', 'profession', 'workpro', 'education')

    # 实现workpro的数据获取
    def get_workpro(self, obj):
        resume_id = obj
        resume_listobj = HrResumeWorkprocess.objects.filter(pk_id=str(resume_id)).all()
        if not resume_listobj:
            resume_listobj = HrTempWorkprocess.objects.filter(pk_id=str(resume_id)).all()

        work_listobj = ResumeWorkproSerializer(resume_listobj, many=True).data

        return work_listobj

    # 实现education的数据获取
    def get_education(self, obj):
        resume_id = obj
        resume_listobj = HrResumeEducation.objects.filter(pk_id=str(resume_id)).all().order_by('-out_school_date')
        if not resume_listobj:
            resume_listobj = HrTempEducation.objects.filter(pk_id=str(resume_id)).all().order_by('-out_school_date')

        edu_listobj = ResumeEduSerializer(resume_listobj, many=True).data

        return edu_listobj
