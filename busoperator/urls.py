from django.contrib import admin
from django.urls import path,include

from .views import *

urlpatterns = [
    path('bus/',BusCreateView.as_view()),
    path('bus/<bus_no>',BusGeneric.as_view()),
    path('driver/',DriverCreateView.as_view()),
    path('driver/<id>',DriverGeneric.as_view()),
    path('bus-stop/',BusStopCreateView.as_view()),
    path('bus-stop/<id>',BusStopGeneric.as_view()),
    path('bus-schedule/',ScheduleCreateView.as_view()),
    path('bus-schedule/<id>',ScheduleGeneric.as_view()),
]