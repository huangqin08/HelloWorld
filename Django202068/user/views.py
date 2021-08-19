from django.shortcuts import render, redirect
from django.http import HttpResponse


# Create your views here.
articles = ['文章首页1','文章首页2','文章首页3']


def index(request):
    return HttpResponse('<b1>我的第一个博客<b1/>')

def article(request,num):
    return HttpResponse(articles[num-1])

def show_article(request,name):
    return HttpResponse('文章:'+ name)


