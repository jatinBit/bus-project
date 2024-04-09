from django.db import models

# Create your models here.
class Bus(models.Model):
    bus_no=models.CharField(max_length=4,primary_key=True)

    def __str__(self):
        return self.bus_no

class Driver(models.Model):
    name=models.CharField(max_length=50,null=False,blank=False)
    phone_no=models.CharField(max_length=10,unique=True,null=False,blank=False)
    aadhaar_no=models.CharField(max_length=12,unique=True,null=False,blank=False)
    licence_no=models.CharField(max_length=16,unique=True,null=False,blank=False)
    age=models.IntegerField(null=False,blank=False)
    address=models.TextField(null=False,blank=False)

    def __str__(self):
        return self.name

class BusStop(models.Model):
    name=models.CharField(max_length=100,unique=True,null=False,blank=False)

    def __str__(self):
        return self.name
    
class Schedule(models.Model):
    depart_from=models.ForeignKey(BusStop,on_delete=models.CASCADE)
    destination=models.ForeignKey(BusStop,on_delete=models.CASCADE, related_name='destination')
    start_time=models.TimeField(null=False,blank=False)
    end_time=models.TimeField(null=False,blank=False)
    driver=models.ForeignKey(Driver,null=True,blank=True,on_delete=models.CASCADE)
    bus=models.ForeignKey(Bus,null=True,blank=True,on_delete=models.CASCADE)
    mon=models.BooleanField(default=False)
    tue=models.BooleanField(default=False)
    wed=models.BooleanField(default=False)
    thu=models.BooleanField(default=False)
    fri=models.BooleanField(default=False)
    sat=models.BooleanField(default=False)
    sun=models.BooleanField(default=False)

    PURPOSE_CHOICES=(
        ('staff','staff'),
        ('school','school'),
        ('student','student')
    )

    purpose=models.CharField(max_length=7,null=False,blank=False,choices=PURPOSE_CHOICES)

    def __str__(self):
        id=str(self.id)
        return id
    
