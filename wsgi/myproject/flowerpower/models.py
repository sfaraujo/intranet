#!/usr/bin/python
# -*- coding: latin-1 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, Group

class ParrotAuth(models.Model):
	username = models.CharField(max_length=255,)
	password = models.CharField(max_length=255,)
	client_id = models.CharField(max_length=255,)
	client_secret = models.CharField(max_length=255,)
	user = models.ForeignKey(User)
	
	def __unicode__(self):
		return unicode(self.username)
		
class Sensor(models.Model):
	sensor_serial = models.CharField(max_length=255,)
	plantnickname = models.CharField(max_length=255, blank=True)
	group = models.ForeignKey(Group, null=True, blank=True)
	
	def __unicode__(self):
		return unicode(self.plantnickname)

class Location(models.Model):
	air_temperature = models.DecimalField(max_digits=12, decimal_places=10, null=True, blank=True)
	air_temperature_text = models.CharField(max_length=255, blank=True)
	battery = models.DecimalField(max_digits=3, decimal_places=0, null=True, blank=True)
	fertilizer = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
	fertilizer_text = models.CharField(max_length=255, blank=True)
	fertilizer_last_sample = models.DateTimeField(null=True, blank=True)
	light = models.DecimalField(max_digits=15, decimal_places=12, null=True, blank=True)
	light_text = models.CharField(max_length=255, blank=True)
	total_samples_count = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	status_creation_datetime_utc = models.DateTimeField(null=True, blank=True)
	last_sample_utc = models.DateTimeField(null=True, blank=True)
	last_sample_upload = models.DateTimeField(null=True, blank=True)
	soil_moisture = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
	soil_moisture_text = models.CharField(max_length=255, blank=True)
	avatar_url = models.CharField(max_length=255, blank=True)
	latitude = models.CharField(max_length=255, blank=True)
	longitude = models.CharField(max_length=255, blank=True)
	location_identifier = models.CharField(max_length=255, blank=True)
	sensor_serial = models.CharField(max_length=255, blank=True)
	plant_nickname = models.CharField(max_length=255, blank=True)
	group = models.ForeignKey(Group, null=True, blank=True)
	
	def __unicode__(self):
		return self.plant_nickname
		

class Sample(models.Model):
	air_temperature_celsius = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	battery_percent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	capture_datetime_utc = models.DateTimeField(db_index=True, null=True)
	fertilizer_level = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	light = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	soil_moisture_percent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	sensor = models.ForeignKey(Location, unique=False, null=True, blank=True)

	
	def __unicode__(self):
		return unicode(self.capture_datetime_utc)
		
class Evapotranspiration(models.Model):
	value = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
	date = models.DateTimeField(null=True)
	
	def __unicode__(self):
		return unicode(self.date)
	