#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   TimeRel.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/8/25 15:49   gxrao      1.0         None
'''
import logging
from datetime import datetime

logger = logging.getLogger('log')

def released_time(value):
    """自定义发布时间过滤器"""
    created_time = value.timestamp()  # 把发布时间转换成秒级时间戳
    now_time = datetime.now().timestamp()  # 获取当前时间戳（秒级）
    duration = now_time - created_time
    if duration < 60:  # 小于一分钟
        display_time = "刚刚"
    elif duration < 60 * 60:  # 小于一小时
        display_time = str(int(duration / 60)) + "分钟前"
    elif duration < 60 * 60 * 24:  # 小于24小时
        display_time = str(int(duration / 60 / 60)) + "小时前"
    elif duration < 60 * 60 * 24 * 30:  # 小于30天
        display_time = str(int(duration / (60 * 60 * 24))) + "天前"
    else:
        display_time = value.strftime('%Y-%m-%d')  # 大于30天
    logger.debug('时间转换：{}'.format(display_time))
    return display_time  # 返回显示结果