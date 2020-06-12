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


class IndexView(ListView):

    import requests
    import datetime
    r=requests.get('http://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=b13bc69dfb1da2ace7b8a62928fef4f0')
    payload = json.loads(r.text)
    print(payload)
    weather= payload["main"]["temp"] #- 273.15
    we_с = weather - 273
    place=payload["name"]
    now = datetime.datetime.now()
    template_name = "index/index.html"
    extra_context={"w": [place,we_с,str(now)]}
    p=Weather(data=now, we=weather, city=place)
    if not p.same_data:
        p.save()
    model=Weather





# def get(self,request):
#    return render(request, "index/index.html")
