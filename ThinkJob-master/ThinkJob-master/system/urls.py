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
from system.views import *

# 子路由信息
app_name = 'system'

urlpatterns = [
    path('search_criteria', search_criteria, name='search_criteria'),  # 获取所有高级搜索的key与value
    path('message_code', message_code, name='message_code'),  # 获取短信验证码
    path('img_code', img_code, name='img_code'),  # 获取图片验证码
    path('tradenews_list', tradenews_list, name='tradenews_list'),  # 行业数据新闻列表
    path('tradenews_detail', tradenews_detail, name='tradenews_detail'),  # 行业数据新闻详情
    path('XLS_update', XLS_update, name='XLS_update'),  # XLS的数据导入
    path('data_statistics', data_statistics, name='data_statistics'), # 大屏数据统计
]
