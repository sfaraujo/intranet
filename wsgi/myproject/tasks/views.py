#!/usr/bin/python
# -*- coding: latin-1 -*-
from django.shortcuts import render
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime, date
from fertilize.models import DayPortion, Culture, DayPortionProduct
from django.core import serializers
import json
from flowerpower.views import localtime
from datetime import datetime
from flowerpower.models import Sensor
from django.contrib.auth.models import User, Group
from decimal import *
from django.db.models import F, FloatField, Sum



@login_required
def tasks(request):
    sensors = []
    if request.user.is_superuser:
        sensors = Sensor.objects.all()
    else:
        groups = Group.objects.filter(user=request.user)
        for group in groups:
            sensors += Sensor.objects.filter(group=group)
    if request.GET.get("all") == 'true':
        tasks = Task.objects.all()
        workDays = WorkDay.objects.all()
    else:
        tasks = Task.objects.exclude(state=State.objects.get(pk=3))
        workDays = WorkDay.objects.exclude(task__state=State.objects.get(pk=3))
    taskCategories = TaskCategory.objects.all()
    dayPortions = DayPortion.objects.exclude(state=State.objects.get(pk=3))
    states = State.objects.all()
    locales = Local.objects.all()
    years = Task.objects.all().dates('startDate', 'year')
    graphData = list()
    year_list = list()
    year_durations = list()
    cat_list = list()
    locales_list = list()
    for year in years:
        year_list.append(year.year)
    for local in locales:
        locales_list.append(local.name)
        for year in years:
            tasksByYear = Task.objects.filter(local=local, startDate__year=year.year)
            y_duration = tasksByYear.aggregate(duration=Sum('duration'))
            year_durations.append([local.name,year.year,y_duration['duration']])
            for category in taskCategories:
                tasksByCategory = tasksByYear.filter(category=category).annotate(Sum('duration'))
                try:
                    category = tasksByCategory[0].category
                    duration = tasksByCategory.aggregate(duration=Sum('duration'))
                    cat_list.append([local.name,year.year,category,duration['duration']])
                except:
                    pass
        
        graphData.append([local.name,year_list])

    context = {'workDays':workDays,'locales_list':locales_list,'cat_list':cat_list,'year_durations':year_durations,'year_list':year_list,'graphData':graphData,'states':states,'locales':locales,'taskCategories':taskCategories,'dayPortions':dayPortions,'tasks' : tasks,'sensors':sensors}
    return render(request,'tasks.html', context)


@login_required
def getTasks(request):
    if request.GET.get("all") == 'true':
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.exclude(state=State.objects.get(pk=3))
        
    data = serializers.serialize('json', tasks, indent=2, use_natural_foreign_keys=True)
    
    #data = json.dumps([w.get_json() for w in WorkDay.objects.all()])
    
    return HttpResponse(data, content_type='application/json')
    
@login_required
def saveTask(request):
    if request.method == 'POST':
        alldata=request.POST
        event_index = alldata.get("event-index", "0")
        startDate = alldata.get("event-start-date", "0")
        endDate = alldata.get("event-end-date", "0")
        startDate = datetime.strptime(startDate,"%m/%d/%Y")
        endDate = datetime.strptime(endDate,"%m/%d/%Y")
        category = alldata.get("event-category", "0")
        state = alldata.get("event-state", "")
        local = alldata.get("event-local", "0")
        if state != "" or alldata.get("event-location", "0") != "":
            if event_index == '':
                form_obj = Task.objects.create()
            else:
                form_obj, created = Task.objects.get_or_create(pk=int(event_index))
            form_obj.name = alldata.get("event-name", "0")
            
            form_obj.local = Local.objects.get(name=local)
            form_obj.category = TaskCategory.objects.get(name=category)
            form_obj.description = alldata.get("event-description", "0")
            form_obj.state = State.objects.get(name=state)
            form_obj.field_book = alldata.get("event-field_book", "0")
            form_obj.startDate = startDate
            form_obj.endDate = endDate
            form_obj.persons = int(alldata.get("event-persons", "0"))
            form_obj.duration = Decimal(alldata.get("event-duration", "0"))*int(alldata.get("event-persons", "0"))
            
            form_obj.save()
            
            #workDay_obj, created2 = WorkDay.objects.get_or_create(task=form_obj, startDate=startDate)
            
            #workDay_obj.startDate = startDate
            #workDay_obj.endDate = endDate
            #workDay_obj.persons = int(alldata.get("event-persons", "0"))
            #workDay_obj.duration = Decimal(alldata.get("event-duration", "0"))
            #workDay_obj.save()
        payload = {'success': True}
        return HttpResponse(json.dumps(payload), content_type='application/json')

@login_required
def deleteTask(request):
    id = request.POST.get('id', '')
    task = Task.objects.get(pk = int(id))
    task.delete()
    payload = {'success': True}
    return HttpResponse(json.dumps(payload), content_type='application/json')
    
    

@login_required
def saveWorkDay(request):
    if request.method == 'POST':
        alldata=request.POST
        event_index = alldata.get("event-index", "0")
        print event_index
        task = Task.objects.get(pk=int(event_index))
        startDate = alldata.get("event-start-date", "0")
        endDate = alldata.get("event-end-date", "0")
        startDate = datetime.strptime(startDate,"%m/%d/%Y")
        endDate = datetime.strptime(endDate,"%m/%d/%Y")
            
        workDay_obj, created = WorkDay.objects.get_or_create(task=task, startDate=startDate)
        workDay_obj.startDate = startDate
        workDay_obj.endDate = endDate
        workDay_obj.persons = int(alldata.get("event-persons", "0"))
        workDay_obj.duration = Decimal(alldata.get("event-duration", "0"))*int(alldata.get("event-persons", "0"))
        workDay_obj.save()
        task.duration = task.duration + workDay_obj.duration
        task.save()
        payload = {'success': True}
        return HttpResponse(json.dumps(payload), content_type='application/json')


@login_required
def deleteWorkDay(request):
    print request.POST
    id = request.POST.get('id', '')
    print id
    wk = WorkDay.objects.get(pk=int(id))
    task = Task.objects.get(pk = wk.task.pk)
    print task.duration
    task.duration = task.duration - wk.duration
    task.save()
    wk.delete()
    payload = {'success': True}
    return HttpResponse(json.dumps(payload), content_type='application/json')
    

