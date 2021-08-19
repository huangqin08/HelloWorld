#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ThisWeek.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/9/22 14:59   gxrao      1.0         None
'''
import datetime
from datetime import timedelta


def thisweek(date):
    now = datetime.datetime.strptime(date, '%Y-%m-%d')

    # 本周第一天和最后一天
    this_week_one = now - timedelta(days=now.weekday())
    this_week_two = now + timedelta(days=1 - now.weekday())
    this_week_three = now + timedelta(days=2 - now.weekday())
    this_week_four = now + timedelta(days=3 - now.weekday())
    this_week_five = now + timedelta(days=4 - now.weekday())
    this_week_six = now + timedelta(days=5 - now.weekday())
    this_week_serven = now + timedelta(days=6 - now.weekday())
    this_week_list = [this_week_one,this_week_two,this_week_three,this_week_four,this_week_five,this_week_six,this_week_serven]

    return this_week_list

# time_obj = []
# obj = thisweek('2020-09-22')
# for i in obj:
#     time_obj.append(str(i.strftime('%Y-%m-%d')))
# print(time_obj)