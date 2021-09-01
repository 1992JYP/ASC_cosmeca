from django.urls.base import reverse_lazy
from apps.main.Crawlers.naverCrawler import naverCrawler
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from django.views import View
from apps.paradise import models as lpmodels
from apps.main import models
from django.urls import reverse
from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
# from bs4 import BeautifulSoup
import time
import pandas as pd
# from tqdm import tqdm_notebook
# from selenium.webdriver.common.alert import Alert4
from apps.main.Crawlers.naverCrawler import naverCrawler

from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    Query = lpmodels.CpProduct.objects.filter(keyword='안전문')
    template = loader.get_template('main/home.html')
    context = {
        'some_dynamic_value': 'This text comes from django view!',
        'test' : Query
    }
    return HttpResponse(template.render(context, request))
@login_required
def main(request):
    Query = lpmodels.ProductMaster.objects.all()
    template = loader.get_template('main/main.html')
    context = {
        'some_dynamic_value': 'This text comes from django view!',
        'Query' : Query
    }
    return HttpResponse(template.render(context, request))

@login_required
def keyword(request):
    keyword = request.GET.get('keyword')
    print(keyword)
    rank_today = lpmodels.CpProduct.objects.filter(date_info__lt='2021-08-06').filter(date_info__gte='2021-08-05').order_by('keyword').order_by('pd_index')
    rank_today_others = lpmodels.CpProduct.objects.filter(keyword=keyword).filter(date_info__gte='2021-07-08').exclude(title__icontains='아가드').exclude(title__icontains='생활낙원')[:3]
    template = loader.get_template('main/keyword.html')
    context = {
        'some_dynamic_value': 'This text comes from django view!',
        'ranking' : rank_today,
        'ranking_others_coup' : rank_today_others
    }
    return HttpResponse(template.render(context, request))

@login_required
def review(request):
    template = loader.get_template('main/review.html')
    context = {
        'some_dynamic_value': 'This text comes from django view!',
    }
    return HttpResponse(template.render(context, request))

@login_required
def     Dashboard(request):
    rankingchange = lpmodels.CpProduct.objects.filter(date_info__gte='2021-07-22').filter(title__icontains='아가드').exclude(change_index=0).order_by('pd_index')[:10]
    title = request.GET.get('title')
    # if title:
    #     chart=lpmodels.CpProduct.objects.filter(title=title).filter(date_info__gte='2021-07-02')
    #     chart=list(chart)
    # else:
    #     firstdata   =   lpmodels.CpProduct.objects.filter(title__icontains='아가드').filter(date_info__gte='2021-07-08').filter(title__icontains='아가드').exclude(change_index=0).order_by('pd_index').only('title')[:1]
  
    #     chart       =   lpmodels.CpProduct.objects.filter(title=firstdata).filter(date_info__gte='2021-07-02').order_by('date_info').only('pd_index')


    # print(chart[0])
    template = loader.get_template('main/Dashboard.html')
    context = {
        'some_dynamic_value': 'This text comes from django view!',
        'rankingchange' : rankingchange,
        # 'chart' :chart
    }
    return HttpResponse(template.render(context, request))

@login_required
def dbtest(request):



    # dbtesttext.delete()
    namequery = request.POST.get('name','')
    posquery = request.POST.get('position','')
    phonequery = request.POST.get('phone','')
    # namequery = request.POST['btntest123']a
    # cs = naverCrawler()
    # print(cs.fcrawgo())
    if request.POST.get('btncheck','')=='1':
        dbtesttext = models.Employees.objects.filter(name=namequery)
  
    elif request.POST.get('btncheck','')=='2':
        dbtesttext = models.Employees.objects.create(name=namequery,position=posquery,phone=phonequery)
        dbtesttext = models.Employees.objects.all()
    else:    
        dbtesttext = models.Employees.objects.all()

    template = loader.get_template('main/dbtest.html')
    context = {
        'some_dynamic_value': 'This text comes from django view!',
        'test' : dbtesttext,
        'name' : '''namequery'''
        # 'modeltest' : modeltest
        # 'testtext' : request
    }
    return HttpResponse(template.render(context, request))



@login_required
def login(request):
    template = loader.get_template('main/login.html')
    context = {
        'some_dynamic_value': 'This text comes from django view!',
    }
    return HttpResponse(template.render(context, request))




@login_required
def review_Dashboard(request):
    template = loader.get_template('main/review_Dashboard.html')
    context = {
        'some_dynamic_value': 'This text comes from django view!',
    }
    return HttpResponse(template.render(context, request))

# def home(request):
#     template = loader.get_template('main/home.html')
#     context = {
#         'key_number': '1',
#         'key_rank' : '순위1',
#         'review_number': '1',
#         'review_rank' : '순위1',
#     }
#     return HttpResponse(template.render(context, request))


    
    
    



# def home_key(request):
#     keyword = '안전문'
#     Query = lpmodels.CpProduct.objects.filter(keyword='안전문').filter(date_info__gte='2021-07-05').exclude(change_index=0).exclude(change_index=9999)[:7]
#     template = loader.get_template('main/home_key.html')
#     context = {
#         'some_dynamic_value': 'This text comes from django view!',
#         'test' : Query
#     }
#     return HttpResponse(template.render(context, request))

# def home_review(request):
#     template = loader.get_template('main/home_review.html')
#     context = {
#         'some_dynamic_value': 'This text comes from django view!',
#     }
#     return HttpResponse(template.render(context, request))


# def home_review_search(request):
    template = loader.get_template('main/home_review_search.html')
    context = {
        'some_dynamic_value': 'This text comes from django view!',
    }
    return HttpResponse(template.render(context, request))

def dbtest(request):
    # dbtesttext.delete()
    namequery = request.POST.get('name','')
    posquery = request.POST.get('position','')
    phonequery = request.POST.get('phone','')
    # namequery = request.POST['btntest123']
    # cs = naverCrawler()
    # print(cs.fcrawgo())
    if request.POST.get('btncheck','')=='1':
        dbtesttext = models.Employees.objects.filter(name=namequery)
  
    elif request.POST.get('btncheck','')=='2':
        dbtesttext = models.Employees.objects.create(name=namequery,position=posquery,phone=phonequery)
        dbtesttext = models.Employees.objects.all()
    else:    
        dbtesttext = models.Employees.objects.all()

    template = loader.get_template('main/dbtest.html')
    context = {
        'some_dynamic_value': 'This text comes from django view!',
        'test' : dbtesttext,
        'name' : '''namequery'''
        # 'modeltest' : modeltest
        # 'testtext' : request
    }
    return HttpResponse(template.render(context, request))



class ModelCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('')
    template_name = "main/create.html"

