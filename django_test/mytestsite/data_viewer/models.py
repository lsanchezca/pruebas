from django.db import models

# Create your models here.

class DataEntry(models.Model):
    truck_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    weight = models.FloatField()
    payload_kg = models.FloatField(null=True, blank=True)

class bin(models.Model):
    bin_id = models.CharField(max_length=100)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return f"{self.truck_id}: {self.weight} at {self.timestamp}"