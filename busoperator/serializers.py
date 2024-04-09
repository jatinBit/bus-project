from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import *

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bus
        fields='__all__'

    def validate_bus_no(self, value):
        for i in value:
            if not i.isdigit():
                raise ValidationError('bus should conatin only digit/numbers')
        if len(value)!=4:
            raise ValidationError('bus no should be of length 4')
        return value

def validPhoneNo(num):
    if(len(num)!=10): 
        return False 
    for i in num:
           if not i.isdigit():
                return False
    return True

def validAadhaarNo(num):
    if(len(num)!=12): 
        return False 
    for i in num:
           if not i.isdigit():
                return False
    return True

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model=Driver
        fields='__all__'

    def validate(self, attrs):
        name=attrs['name']
        phnNo=attrs['phone_no']
        aadhaarNo=attrs['aadhaar_no']
        age=attrs['age']
        licence_no=attrs['licence_no']

        for i in name:
            if not i.isalpha():
                raise ValidationError('name should contain letters only')

        if(not validPhoneNo(phnNo)):
            raise ValidationError('enter a valid phone no.')
        if(not validAadhaarNo(aadhaarNo)):
            raise ValidationError('enter a valid Aadhaar no.')
        if(age<18):
            raise ValidationError('Age should be greater than 18')
        if(len(licence_no)!=16):
            raise ValidationError('enter a valid licence no.')
        return attrs

class BusStopSerializer(serializers.ModelSerializer):
    class Meta:
        model=BusStop
        fields='__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    # driver=DriverSerializer()
    # bus=BusSerializer()
    # depart_from=BusStopSerializer()
    # destination=BusStopSerializer()

    class Meta:
        model=Schedule
        fields='__all__'

    def validate(self, attrs):
        depart_from=attrs['depart_from']
        destination=attrs['destination']
        if(depart_from==destination):
            raise serializers.ValidationError({'stopError':'choose different starting and ending stop'})
        
        start_time=attrs['start_time']
        end_time=attrs['end_time']
        if(start_time==end_time):
            raise serializers.ValidationError({'timeError':'start time and end time should be different'})

        if(not attrs['mon'] and not attrs['tue'] and not attrs['wed'] and not attrs['thu'] and not attrs['fri'] and not attrs['sat'] and not attrs['sun']):
            raise ValidationError({'dayError':"at least one day should be selected"})

        return attrs
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['driver'] = DriverSerializer(instance.driver).data
        response['bus'] = BusSerializer(instance.bus).data
        response['depart_from'] = BusStopSerializer(instance.depart_from).data
        response['destination'] = BusStopSerializer(instance.destination).data
        return response