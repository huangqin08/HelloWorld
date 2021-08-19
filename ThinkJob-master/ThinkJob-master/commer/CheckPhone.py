#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   CheckPhone.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/8/10 10:53   gxrao      1.0         None
'''
from userhr.models import SysMember

def phone_check(phone):
    '''
        checkphone
        :param phone 需要校验的用户手机号
        :return True or False  true用户可以注册，false已存在该用户
    '''
    userphone = SysMember.objects.filter(phone=phone).first()
    if userphone:
        return False;
    else:
        return True;