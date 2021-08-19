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
from resume.views import *

# 子路由信息
app_name = 'resume'

urlpatterns = [
    path('resume_list_all', resume_list_all, name='resume_list_all'),  # 获取所有简历
    path('resume_search', resume_search, name='resume_search'),  # 简历简历高级搜索
    path('check_resume_auth', check_resume_auth, name='check_resume_auth'),  # 简历核验信息
    path('collect_resumelist', collect_resumelist, name='collect_resumelist'),  # 用户搜藏的简历列表
    path('job_search', job_search, name='job_search'),  # 职位搜索接口
    path('new_resume_list_all', new_resume_list_all, name='new_resume_list_all'),  # 新版获取所有简历
    path('new_resume_search', new_resume_search, name='new_resume_search'),  # 新版简历简历高级搜索
    path('new_job_search', new_job_search, name='new_job_search'),  # 新版职位搜索接口
    path('resume_detail', resume_detail, name='resume_detail'),  # 简历详情信息接口
    path('resume_recommend', resume_recommend, name='resume_recommend'),  # 简历推荐接口
    path('resume_evaluating', resume_evaluating, name='resume_evaluating'),  # 简历评测接口
]
