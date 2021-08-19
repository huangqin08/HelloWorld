"""ThinkJob URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from userhr.views import *

# 子路由信息
app_name = 'userhr'

urlpatterns = [
    path('register', register, name='register'),  # 用户注册接口
    path('checkphone', checkphone, name='checkphone'),  # 注册手机号唯一校验
    path('user_login', user_login, name='user_login'),  # 用户登录接口
    path('editor_user', editor_user, name='editor_user'),  # 用户详情编辑
    path('detail_user', detail_user, name='detail_user'),  # 用户详情获取
    path('checkpassword', checkpassword, name='checkpassword'),  # 用户修改密码
    path('token', token, name='token'),  # 获取token头信息来设置访问令牌
    path('forget_pwd', forget_pwd, name='forget_pwd'),  # 用户忘记密码接口
    path('resume_update', resume_update, name='resume_update'),  # 用户简历上传
    path('user_collect', user_collect, name='user_collect'),  # 用户简历收藏
    path('colldown_status', colldown_status, name='colldown_status'),  # 收藏下载状态查询
    path('user_datastatis', user_datastatis, name='user_datastatis'),  # 用户基本详情数据获取
    path('download_file', download_file, name='download_file'),  # 用户下载简历
    path('look_resume', look_resume, name='look_resume'),  # 简历联系方式查看
    path('user_logout', user_logout, name='user_logout'),  # 用户注销接口
    path('message_login', message_login, name='message_login'),  # 短信验证码登录接口
    path('user_alarm', user_alarm, name='user_alarm'),  # 用户反馈简历信息接口
    path('userupdate_list', userupdate_list, name='userupdate_list'),  # 用户上传简历列表
    path('checkuser_login', checkuser_login, name='checkuser_login'),  # 用户上传简历列表
]
