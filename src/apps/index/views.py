from django import http as h
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
import json
from apps.index.models import Weather
from django.views.generic import ListView
# def view(request: HttpRequest) -> HttpResponse: # это хтнты, валидация типов (то есть их соответствие типов)
# if request.method!="GET":
# not work   return HttpResponse("xxx",status=405)
#    if request.method=="GET":
#       return render(request, "index/index.html") # питон приводит значение к типу прямо на месте тк динамич язык

api_city='London'
class IndexView(ListView):

    '''import requests
    import datetime
    r=requests.get('http://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=b13bc69dfb1da2ace7b8a62928fef4f0')
    payload = json.loads(r.text)
    print(payload)
    weather= payload["main"]["temp"] #- 273.15
    we_с = weather - 273
    place=payload["name"]
    now = datetime.datetime.now()'''
    template_name = "index/index.html"
   # extra_context={"w": [place,we_с,str(now)]}
    #p=Weather(data=now, we=we_с, city=place)
    #if not p.same_data:
     #   p.save()
    model=Weather
    def get_context_data(self, **kwargs):
        parent_ctx = super().get_context_data()
        import requests
        import datetime
        r = requests.get(
            #'http://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=b13bc69dfb1da2ace7b8a62928fef4f0')
            f'http://api.openweathermap.org/data/2.5/weather?q={api_city}&APPID=b13bc69dfb1da2ace7b8a62928fef4f0')
        payload = json.loads(r.text)
        #print(payload)
        weather = payload["main"]["temp"]  # - 273.15
        we_с = weather - 273
        place = payload["name"]
        now = datetime.datetime.now()
        p = Weather(data=now, we=we_с, city=place)
        print(p)
        if p.same_data():
            p.save()
            print("save")
        ctx = {"w": [place,we_с,str(now)]}
        ctx.update(parent_ctx)
        return ctx

from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.index.forms import UpForm



class UpView(FormView):
    template_name = "index/form.html"
    form_class = UpForm
    success_url = reverse_lazy("index:index")
    def form_valid(self, form):
        c = form.cleaned_data.get("city")
        print(c)
        global api_city
        api_city = c
        return super().form_valid(form)

    #@transaction.atomic()
    #def form_valid(self, form):
    #    user = form.save()
     #   start_verification(self.request, user)
      #  return super().form_valid(form)




# def get(self,request):
#    return render(request, "index/index.html")
