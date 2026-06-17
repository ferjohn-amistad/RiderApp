from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = [
        ('admin', 'Admin'),
        ('rider', 'Rider'),
        ('driver', 'Driver'),
    ]

    id_user = models.AutoField(primary_key=True)
    role = models.CharField(max_length=20, choices=ROLES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)

def __str__(self):
    return f"{self.first_name} {self.last_name[0]} ({self.role})"

class Ride(models.Model):
    STATUS = [
        ('en-route', 'En Route'),
        ('pickup', 'Pickup'),
        ('dropoff', 'Dropoff'),
    ]

    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=STATUS)
    id_rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_rider')
    id_driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_driver')
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()

    def __str__(self):
        return f"Ride {self.id_ride} - {self.status}"

class RideEvent(models.Model):
    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='ride_events')
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Event {self.id_ride_event} - Ride {self.id_ride}"