from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class BusCreateView(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Bus.objects.all()
    serializer_class=BusSerializer

class BusGeneric(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Bus.objects.all()
    serializer_class=BusSerializer
    lookup_field='bus_no'

class DriverCreateView(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Driver.objects.all()
    serializer_class=DriverSerializer

class DriverGeneric(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Driver.objects.all()
    serializer_class=DriverSerializer
    lookup_field='id'

class BusStopCreateView(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=BusStop.objects.all()
    serializer_class=BusStopSerializer

class BusStopGeneric(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset=BusStop.objects.all()
    serializer_class=BusStopSerializer
    lookup_field='id'

class ScheduleCreateView(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Schedule.objects.all()
    serializer_class=ScheduleSerializer

class ScheduleGeneric(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Schedule.objects.all()
    serializer_class=ScheduleSerializer
    lookup_field='id'
