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

from resume.models import HrResumeEvaluating
from system.models import SysTradenews

logger = logging.getLogger('log')

class HrResumeEvaluatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HrResumeEvaluating
        # 以下都是显示的值
        fields = ('id', 'news_title', 'news_text', 'create_user', 'create_time')

class SysTradenewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysTradenews
        # 以下都是显示的值
        fields = ('id', 'news_title', 'news_subtitle', 'create_time', 'news_img', 'create_user')

class SysTradenewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysTradenews
        # 以下都是显示的值
        fields = ('id', 'news_title', 'news_subtitle','news_text', 'create_time', 'news_img', 'create_user')