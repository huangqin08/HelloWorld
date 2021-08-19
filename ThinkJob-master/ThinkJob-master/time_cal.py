#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   time_cal.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/9/22 14:57   gxrao      1.0         None
'''
import datetime
from datetime import timedelta

now = datetime.datetime.now()

# 今天
today = now
print('--- today = {}'.format(today))

# 昨天
yesterday = now - timedelta(days=1)
print('--- yesterday = {}'.format(yesterday))

# 明天
tomorrow = now + timedelta(days=1)
print('--- tomorrow = {}'.format(tomorrow))

# 当前季度
now_quarter = now.month / 3 if now.month % 3 == 0 else now.month / 3 + 1
print('--- now_quarter = {}'.format(now_quarter))

# 本周第一天和最后一天
this_week_start = now - timedelta(days=now.weekday())
this_week_end = now + timedelta(days=6 - now.weekday())
print('--- this_week_start = {} this_week_end = {}'.format(this_week_start, this_week_end))

# 上周第一天和最后一天
last_week_start = now - timedelta(days=now.weekday() + 7)
last_week_end = now - timedelta(days=now.weekday() + 1)
print('--- last_week_start = {} last_week_end = {}'.format(last_week_start, last_week_end))

# 本月第一天和最后一天
this_month_start = datetime.datetime(now.year, now.month, 1)
this_month_end = datetime.datetime(now.year, now.month + 1, 1) - timedelta(days=1) + datetime.timedelta(
    hours=23, minutes=59, seconds=59)
print('--- this_month_start = {} this_month_end = {}'.format(this_month_start, this_month_end))

# 上月第一天和最后一天
last_month_end = this_month_start - timedelta(days=1) + datetime.timedelta(
    hours=23, minutes=59, seconds=59)
last_month_start = datetime.datetime(last_month_end.year, last_month_end.month, 1)
print('--- last_month_end = {} last_month_start = {}'.format(last_month_end, last_month_start))

# 本季第一天和最后一天
month = (now.month - 1) - (now.month - 1) % 3 + 1
this_quarter_start = datetime.datetime(now.year, month, 1)
this_quarter_end = datetime.datetime(now.year, month + 3, 1) - timedelta(days=1) + datetime.timedelta(
    hours=23, minutes=59, seconds=59)
print('--- this_quarter_start = {} this_quarter_end = {}'.format(this_quarter_start, this_quarter_end))

# 上季第一天和最后一天
last_quarter_end = this_quarter_start - timedelta(days=1) + datetime.timedelta(
    hours=23, minutes=59, seconds=59)
last_quarter_start = datetime.datetime(last_quarter_end.year, last_quarter_end.month - 2, 1)
print('--- last_quarter_start = {} last_quarter_end = {}'.format(last_quarter_start, last_quarter_end))

# 本年第一天和最后一天
this_year_start = datetime.datetime(now.year, 1, 1)
this_year_end = datetime.datetime(now.year + 1, 1, 1) - timedelta(days=1) + datetime.timedelta(
    hours=23, minutes=59, seconds=59)
print('--- this_year_start = {} this_year_end = {}'.format(this_year_start, this_year_end))

# 去年第一天和最后一天
last_year_end = this_year_start - timedelta(days=1) + datetime.timedelta(
    hours=23, minutes=59, seconds=59)
last_year_start = datetime.datetime(last_year_end.year, 1, 1)
print('--- last_year_start = {} last_year_end = {}'.format(last_year_start, last_year_end))
