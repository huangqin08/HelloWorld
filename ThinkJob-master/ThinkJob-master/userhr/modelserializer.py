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

from resume.models import HrTempBase
from userhr.models import SysMember
logger = logging.getLogger('log')

class SysMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysMember
        # 以下都是显示的值
        fields = ('id', 'user_name', 'company_name', 'link_name',
                  'company_scale', 'e_mail', 'content', 'attention_key', 'update_time', 'update_psn')


# 用户上传列表数据模型序列化
class UpdateUserListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = HrTempBase
        # 以下都是显示的值
        fields = ('create_time', 'file_name', 'status')

    def get_status(self, obj):
        try:
            status = obj.imp_flag
            if status == '0':
                # status = '无效的简历'
                color_code = '0'
                logger.info('这个{}简历的具体状态为：{}'.format(obj.id, '没有电话'))
                status = '无效的简历：没有电话'
            elif status == '1':
                # status = '无效的简历'
                color_code = '0'
                logger.info('这个{}简历的具体状态为：{}'.format(obj.id, '电话错误'))
                status = '无效的简历：电话错误'
            elif status == '2':
                # status = '无效的简历'
                color_code = '0'
                logger.info('这个{}简历的具体状态为：{}'.format(obj.id, '没有姓名'))
                status = '无效的简历：没有姓名'
            elif status == '8':
                # status = '无效的简历'
                color_code = '0'
                logger.info('这个{}简历的具体状态为：{}'.format(obj.id, '解析失败'))
                status = '无效的简历：解析失败'
            elif status == '9':
                # status = '重复上传'
                color_code = '1'
                logger.info('这个{}简历的具体状态为：{}'.format(obj.id, '重复上传'))
                status = '无效的简历：重复上传'
            else:
                status = '无效的简历'
                color_code = '0'
                logger.info('这个{}简历的具体状态为：{}'.format(obj.id, '无状态'))
        except:
            integral = obj.integral
            status = obj.status
            if status == None:
                status = '上传成功+{}分，简历待审核'.format(integral)
                color_code = '2'
            elif status == '0':
                status = '无效的简历：审核无效'
                color_code = '0'
                logger.info('这个{}简历的具体状态为：{}'.format(obj.id, '无状态0'))
            elif status == '1':
                status = '上传成功+{}分，审核通过'.format(integral)
                color_code = '2'
            elif status == '2':
                status = '上传成功+{}分，简历待审核'.format(integral)
                color_code = '2'
            elif status == '3':
                status = '无效的简历：审核无效'
                color_code = '0'
                logger.info('这个{}简历的具体状态为：{}'.format(obj.id, '无状态3'))
        return status, color_code
