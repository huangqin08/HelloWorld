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
from django.contrib import admin
from django.urls import path, include

# 主路由信息
# from userhr.views import test
from userhr.views import test

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('test',test),
    path('api2/userhr/', include('userhr.urls' , namespace='userhe')), # 用户相关的路由信息
    path('api2/resume/', include('resume.urls' , namespace='resume')), # 获取简历相关路由信息
    path('api2/system/', include('system.urls' , namespace='system')), # 获取系统相关路由信息
    path('api2/backstage/', include('backstage_ment.urls' , namespace='backstage')),  # 后台管理接口路由
]
