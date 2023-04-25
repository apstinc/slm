
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from .views import home
from DjangoDash.dash_apps.finished_apps import simpleexample


urlpatterns = [
    path('',home)
    # path('', views.)

]