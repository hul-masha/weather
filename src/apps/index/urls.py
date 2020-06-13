from django.urls import path
from django.views.generic import TemplateView

from apps.index.apps import IndexConfig
from apps.index.views import IndexView
from apps.index.views import UpView

app_name = IndexConfig.label

urlpatterns = [
    path("f/", IndexView.as_view(), name="index",),
    path("", UpView.as_view(), name="f",),
]
