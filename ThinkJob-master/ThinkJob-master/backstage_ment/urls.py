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

from backstage_ment.views_resumedel import resumedel
from backstage_ment.views_resumeedit import resumeedit
from backstage_ment.views_resumelist import resumelist

# 子路由信息
app_name = 'backstage_ment'

urlpatterns = [
    path('resumelist',resumelist,name='resumelist'), #后台管理简历列表
    path('resumeedit',resumeedit,name='resumeedit'), #简历编辑
    path('resumedel',resumedel,name='resumedel'), #简历编辑
]
