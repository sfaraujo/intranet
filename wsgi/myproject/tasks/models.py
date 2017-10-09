#!/usr/bin/python
# -*- coding: latin-1 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class TaskCategory(models.Model):
    name = models.CharField(max_length=255,)
    
    def __unicode__(self):
        return unicode(self.name)
    
    def natural_key(self):
        return (self.name)
		
class State(models.Model):
    name = models.CharField(max_length=255,)
    
    def __unicode__(self):
        return unicode(self.name)

    def natural_key(self):
        return (self.name)
        
class Local(models.Model):
    name = models.CharField(max_length=255,)
    
    def __unicode__(self):
        return unicode(self.name)

    def natural_key(self):
        return (self.name)
		
class Task(models.Model):
    name = models.CharField(max_length=255,)
    description = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(TaskCategory, null=True, blank=True)
    #location = models.CharField(max_length=255, blank=True)
    local = models.ForeignKey(Local, null=True, blank=True)
    startDate = models.DateTimeField(null=True, blank=True)
    endDate = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    state = models.ForeignKey(State, null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    field_book = models.CharField(max_length=255,)
    persons = models.IntegerField(null=True, blank=True, default='0')
    duration = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default='0')

    def __unicode__(self):
        return unicode(self.name)

    def natural_key(self):
        return (self.name)
        
    

class WorkDay(models.Model):
    task = models.ForeignKey(Task, null=True, blank=True)
    startDate = models.DateTimeField(null=True, blank=True)
    endDate = models.DateTimeField(null=True, blank=True)
    persons = models.IntegerField(null=True, blank=True, default='0')
    duration = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default='0')
	
    def __unicode__(self):
        return unicode(self.task) + ' - ' + unicode(self.startDate) + ' - ' + unicode(self.endDate)

    def get_json(self):
        return {
            'id': self.task.id,
            'task': str(self.task.name),
            'startDate': str(self.startDate),
            'endDate': str(self.endDate),
            'local':str(self.task.local),
            'category':str(self.task.category),
            'state':str(self.task.state),
            'field_book':self.task.field_book,
            'persons':int(self.persons),
            'duration':float(self.duration),
             }
