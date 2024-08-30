# Inside data_portal_app/models.py

from django.db import models

class BirdFluData(models.Model):
    start_date_collected = models.DateField()
    end_date_collected = models.DateField()
    region = models.CharField(max_length=100, default='Unknown')
    iso_code = models.CharField(max_length=10, default='Unknown')
    country_code = models.CharField(max_length=10, default='Unknown')
    country = models.CharField(max_length=100, default='Unknown')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    hpai_strain = models.CharField(max_length=100, default='Unknown')
    woah_classification = models.CharField(max_length=100, default='Unknown')
    new_outbreaks = models.IntegerField(default=0.0)
    cumulative_outbreaks = models.IntegerField(default=0.0)

    def __str__(self):
        return f"{self.country} - {self.start_date_collected} to {self.end_date_collected}"

class NewData(models.Model):
    fid = models.IntegerField()
    species = models.CharField(max_length=255, default='Unknown')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    date = models.DateField()

    def __str__(self):
        return f"{self.species} - {self.date}"