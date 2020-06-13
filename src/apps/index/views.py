import datetime
import json

from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView
from dynaconf import settings

from apps.index.forms import UpForm
from apps.index.models import Weather

api_city = "London"
nw = datetime.datetime.now()


class IndexView(ListView):

    template_name = "index/index.html"
    # extra_context={"w": [place,we_с,str(now)]}
    # p=Weather(data=now, we=we_с, city=place)
    # if not p.same_data:
    #   p.save()
    model = Weather

    def get_context_data(self, **kwargs):
        parent_ctx = super().get_context_data()
        k = same_data(nw, api_city)
        if k:
            ctx = {"w": [api_city, k.we, str(k.data)]}
        else:
            import requests

            r = requests.get(
                #'http://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=b13bc69dfb1da2ace7b8a62928fef4f0')
                f"http://api.openweathermap.org/data/2.5/weather?q={api_city}&APPID={settings.API_KEY}"
            )
            payload = json.loads(r.text)
            # print(payload)
            weather = payload["main"]["temp"]  # - 273.15
            we_с = weather - 273
            place = payload["name"]
            now = datetime.datetime.now()
            p = Weather(data=now, we=we_с, city=place)
            print(p)
            if p.same_data_city():
                p.save()
                print("save")
            ctx = {"w": [place, we_с, str(now)]}
        ctx.update(parent_ctx)
        return ctx


class UpView(FormView):
    template_name = "index/form.html"
    form_class = UpForm
    success_url = reverse_lazy("index:index")

    def form_valid(self, form):
        c = form.cleaned_data.get("city")
        print(c)
        global api_city, nw
        api_city = c
        nw = form.cleaned_data.get("dat")
        print(nw)
        return super().form_valid(form)


def same_data(now_dat, town):
    try:
        for p in Weather.objects.all():
            if p.data.strftime("%d-%m-%Y %H") == now_dat.strftime("%d-%m-%Y %H"):
                if p.city == town:
                    return p
        return False
    except Exception:
        return False
