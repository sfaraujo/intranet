#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import requests
from lxml import html
import re
from pprint import pformat
import json
from .models import *
from myproject import settings
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse as parse_date
import xml.etree.ElementTree as ET
import pytz, datetime
local = pytz.timezone("Europe/Lisbon")
from fertilize.models import *
from django.db.models import Count
from collections import defaultdict
from decimal import *
from django.db.models import Max, Min
import operator
import collections
from tasks.models import Task
from fertilize.models import DayPortion, DayPortionProduct
from django.views.decorators.cache import cache_page

@login_required
def parrot_auth(request, user):
    parrotUser = ParrotAuth.objects.get(user=user)
    username = parrotUser.username
    password = parrotUser.password
    client_id = parrotUser.client_id
    client_secret = parrotUser.client_secret
    
    req = requests.get('https://api-flower-power-pot.parrot.com/user/v1/authenticate',
                   data={'grant_type': 'password',
                         'username': username,
                         'password': password,
                         'client_id': client_id,
                         'client_secret': client_secret,
                        })
    response = req.json() 
	
    # Get authorization token from response
    access_token = response['access_token']
    auth_header = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    return auth_header

def localtime(dt=datetime.now()):
    try:
        local = pytz.timezone("Etc/GMT+1")
        naive = datetime.strptime (format(dt), "%Y-%m-%dT%H:%M:%SZ")
        local_dt = local.localize(naive, is_dst=None)
        local_dt_utc = local_dt.astimezone (pytz.utc)
    except:
        return timezone.now()
    return local_dt_utc.strftime("%Y-%m-%d %H:%M:%S")

def getSensorGroup(sensor_serial):
    sensor = Sensor.objects.get(sensor_serial=sensor_serial)
    return sensor.group


@login_required
def importData(request):
    users = []
    groups = Group.objects.filter(user=request.user)
    for group in groups:
        users += group.user_set.all()
    
    for user in users:
        try:
            auth_header = parrot_auth(request, user)
        except:
            return HttpResponseRedirect('/')
        response1 = ""
        response2 = ""
        response3 = ""
    
        req = requests.get('https://api-flower-power-pot.parrot.com/garden/v1/status',headers=auth_header)
        response = req.json()
        req1 = requests.get('https://api-flower-power-pot.parrot.com/garden/v2/configuration',headers=auth_header)
        response1 = req1.json()
        for location in response['locations']:
            if int(location['total_sample_count']) > 0:
                li = format(location['location_identifier'].encode('utf-8'))
                for location1 in response1['locations']:
                    li1 = format(location1['location_identifier'].encode('utf-8'))
                    if li == li1:
                        sensor_serial = format(location1['sensor']['sensor_serial'].encode('utf-8'))
                        print sensor_serial
                        last_sample_upload = format(location['last_sample_upload'])
                        last_sample_upload_date = datetime.strptime(last_sample_upload, '%Y-%m-%dT%H:%M:%SZ')
                        try:
                            sensor = Sensor.objects.get(sensor_serial=sensor_serial)
                            print sensor
                            lastSampleDate = Sample.objects.filter(sensor=sensor.pk).latest('capture_datetime_utc')
                            #lastSampleDate = lastSample.last_sample_utc
                        except:
                            lastSampleDate = datetime.now() - relativedelta(years=10)
                        loc_obj, created = Location.objects.get_or_create(sensor_serial = sensor_serial)
                        loc_obj.battery = format(location['battery']['gauge_values']['current_value'])
                        #loc_obj.total_samples_count = format(location['total_sample_count'])
                        #loc_obj.status_creation_datetime_utc = format(location['status_creation_datetime_utc'])
                        #loc_obj.last_sample_upload = format(location['last_sample_utc'])
                        #loc_obj.last_sample_utc = format(location['last_sample_utc'])
                        try:
                            loc_obj.group = getSensorGroup(sensor_serial)
                        except:
                            pass
                        loc_obj.location_identifier = format(location1['location_identifier'].encode('utf-8'))
                        loc_obj.save()
                        #try:
                            #loc_obj.air_temperature = format(location['air_temperature']['gauge_values']['current_value'])
                            #loc_obj.air_temperature_text = format(location['air_temperature']['instruction_key'])
                            #loc_obj.fertilizer = format(location['fertilizer']['gauge_values']['current_value'])
                            #loc_obj.fertilizer_text = format(location['fertilizer']['instruction_key'])
                            #loc_obj.fertilizer_last_sample = format(location['last_sample_utc'])
                            #loc_obj.light = format(location['light']['gauge_values']['current_value'])
                            #loc_obj.light_text = format(location['light']['instruction_key'])
                            #loc_obj.soil_moisture = format(location['watering']['soil_moisture']['gauge_values']['current_value'])
                            #loc_obj.soil_moisture_text = format(location['watering']['instruction_key'])
                            #loc_obj.save()
                        #except:
                            #pass
        
        for location1 in response1['locations']:
            if location1['sensor'] != None :
                li = format(location1['location_identifier'].encode('utf-8'))
                sensor_serial = format(location1['sensor']['sensor_serial'].encode('utf-8'))
                loc_obj, created = Location.objects.get_or_create(sensor_serial = sensor_serial)
                try:
                    loc_obj.avatar_url = format(location1['pictures'][0]['url'])
                except:
                    loc_obj.avatar_url = format(location1['avatar_url'])
                loc_obj.save()
                loc_obj.latitude = format(location1['latitude'])
                loc_obj.longitude = format(location1['longitude'])
                loc_obj.plant_nickname = format(location1['plant_nickname'])
                loc_obj.location_identifier = li
                loc_obj.save()
                try:
                    sensor = Sensor.objects.get(sensor_serial=sensor_serial)
                    from_datetime_utc = Sample.objects.filter(sensor = loc_obj).latest('capture_datetime_utc')
                    to_datetime_utc = timezone.now()
                except:
                    from_datetime_utc = "2010-01-01T00:00:00Z"
                    to_datetime_utc = "2030-01-01T00:00:00Z"
                req2 = requests.get('https://api-flower-power-pot.parrot.com/sensor_data/v6/sample/location/' + li, headers=auth_header,
                    params={'from_datetime_utc': from_datetime_utc,
                            'to_datetime_utc': to_datetime_utc})
                response2 = req2.json()
                for sample in response2['samples']:
                    sample_obj, created = Sample.objects.get_or_create(sensor=loc_obj, capture_datetime_utc = format(sample['capture_datetime_utc']))
                    sample_obj.air_temperature_celsius = format(sample['air_temperature_celsius'])
                    sample_obj.battery_percent = format(sample['battery_percent'])
                    if format(sample['fertilizer_level']) == 'None' :
                        sample_obj.fertilizer_level = 0
                    else:
                        sample_obj.fertilizer_level = format(sample['fertilizer_level'])
                    sample_obj.light = format(sample['light'])
                    sample_obj.soil_moisture_percent = format(sample['soil_moisture_percent'])
                    sample_obj.save()
        
    return HttpResponseRedirect('/')
    

@login_required
def getAllSensors(request):
    try:
        auth_header = parrot_auth(request, request.user)
        req = requests.get('https://api-flower-power-pot.parrot.com/garden/v2/configuration',headers=auth_header)
        response = req.json()
        sensors = []
        sensor = []
        for location in response['locations']:
            try:
                sensor.append(format(location['sensor']['sensor_serial']))
                sensor.append(format(location['sensor']['nickname']))
                sensor.append(format(location['avatar_url']))
                sensor.append(format(location['plant_nickname']))
                sensor.append(format(location['longitude']))
                sensor.append(format(location['latitude']))
                try:
                    ss = Sensor.objects.get(sensor_serial=format(location['sensor']['sensor_serial']))
                    sensor.append(ss.group.pk)
                except:
                    pass
                if sensor not in sensors:
                    sensors.append(location)
            except:
                pass
        return sensors
    except:
        return None



@csrf_exempt
@login_required
def configSensors(request):
    if request.user.is_superuser:
        sensors = Sensor.objects.all()
    else:
        sensors = Sensor.objects.filter(group=Group.objects.get(user=request.user))
        
    sensors_to_config = getAllSensors(request)
    groups = Group.objects.filter(user=request.user)

    if request.method == 'POST':
        alldata=request.POST
        sensor_serial = alldata.get("sensor_serial", "0")
        sensor_group_id = alldata.get("group", "0")
        sensor_plantnickname = alldata.get("plantnickname", "0")
        sensor_obj, created = Sensor.objects.get_or_create(sensor_serial = sensor_serial)
        sensor_obj.group = groups.get(pk = sensor_group_id)
        sensor_obj.plantnickname = sensor_plantnickname
        sensor_obj.save()
        
    context = {'sensors' : sensors, 'sensors_to_config' : sensors_to_config, 'groups' : groups}
    return render(request,'configsensors.html', context)


@csrf_exempt
@login_required
def userGroups(request):
    groups = Group.objects.filter(user=request.user)
    sensors = Sensor.objects.all()
    context = {'groups' : groups, 'sensors': sensors}
    return render(request,'usergroups.html', context)

@login_required
def index(request):
    sensors = []
    #if request.user.is_superuser:
    #    sensors = Sensor.objects.all()
    #else:
    #    groups = Group.objects.filter(user=request.user)
    #    for group in groups:
    #        sensors += Sensor.objects.filter(group=group)
    sensors = Sensor.objects.all()
    try:
        parrot_auth = ParrotAuth.objects.get(user=request.user)
    except:
        parrot_auth = None
    try:
        cultures = Culture.objects.all()
    except:
        cultures = None
    now = datetime.now()
    days_timedelta = timedelta(days=7)
    completedTasks = Task.objects.filter(endDate__lt = localtime(now), state=State.objects.get(pk=3)).order_by('-updated_date')[:5]
    nextTasks = Task.objects.filter(startDate__gte = localtime(now), startDate__lt = localtime(now)+days_timedelta).order_by('startDate')
    startedTasks = Task.objects.filter(state=State.objects.get(pk=2))
    expiredTasks = Task.objects.filter(endDate__lt = localtime(now.today()),state=State.objects.get(pk=1)).order_by('startDate')
    nextFertilizations = DayPortion.objects.filter(date__lt = localtime(now)+days_timedelta, state=State.objects.get(pk=1)).order_by('date')
    context = {'cultures' : cultures, 'sensors' : sensors, 'parrot_auth':parrot_auth, 'completedTasks':completedTasks, 'nextTasks':nextTasks, 'startedTasks':startedTasks,'expiredTasks':expiredTasks, 'nextFertilizations':nextFertilizations}
    return render(request,'index.html', context)


@login_required
def sensor(request, **kwargs):
    days = kwargs.get('date','7')
    now = datetime.now()
    days_timedelta = timedelta(days=int(days))
    sensors = []
    if request.user.is_superuser:
        sensors = Sensor.objects.all()
    else:
        groups = Group.objects.filter(user=request.user)
        for group in groups:
            sensors += Sensor.objects.filter(group=group)
    try:
        parrot_auth = ParrotAuth.objects.get(user=request.user)
    except:
        parrot_auth = None
    sensor_id = kwargs.get('sensor_id')
    sensor = Sensor.objects.get(pk=sensor_id)
    try:
        location = Location.objects.get(sensor_serial=sensor.sensor_serial)
        location_id = location.pk
        samples = Sample.objects.filter(sensor=location_id,capture_datetime_utc__gte=localtime(now)-days_timedelta)
    except:
        location = None
        samples = None
    try:
        lastSample = Sample.objects.filter(sensor=location.pk).latest('capture_datetime_utc')
    except:    
        lastSample = None
        
    
    context = {'lastSample':lastSample,'sensors' : sensors, 'sensor' : sensor, 'parrot_auth':parrot_auth,'location' : location, 'samples': samples, 'cultures' : Culture.objects.all()}
    return render(request,'sensor.html', context)


@login_required
def parrotAccount(request):
    msg = ""
    sensors = []
    if request.user.is_superuser:
        sensors = Sensor.objects.all()
    else:
        groups = Group.objects.filter(user=request.user)
        for group in groups:
            sensors += Sensor.objects.filter(group=group)
        
    if request.method == 'GET':
        try:
            parrot_obj = ParrotAuth.objects.get(user=request.user)
        except:
            parrot_obj = None
        
    if request.method == 'POST':
        alldata=request.POST
        parrot_obj, created = ParrotAuth.objects.get_or_create(user = request.user)
        parrot_obj.username = alldata.get("p_username", "0")
        parrot_obj.password = alldata.get("p_password", "0")
        parrot_obj.client_id = alldata.get("client_id", "0")
        parrot_obj.client_secret = alldata.get("client_secret", "0")
        parrot_obj.save()
        try:
            parrot_auth(request)
        except:
            msg = "Erro de conexão com a API da Parrot Flower Power"

    context = {'sensors' : sensors, 'parrot' : parrot_obj, 'msg': msg}
    return render(request,'parrotaccount.html', context)
    


@login_required
def evapotranspiracao(request):
    Evapotranspirations = Evapotranspiration.objects.all()
    context = {'Evapotranspirations' : Evapotranspirations}
    return render(request,'evapotranspiracao.html', context)

@login_required
def temperaturas(request):
    sensors = []
    if request.user.is_superuser:
        sensors = Sensor.objects.all()
    else:
        groups = Group.objects.filter(user=request.user)
        for group in groups:
            sensors += Sensor.objects.filter(group=group)

    totalColdHours = []

    now = datetime.now()
    locations = Location.objects.all()
    for location in locations:
        monthColdHours = {}
        anualColdHours = {}
        monthTemps = []
        anualTemps = []
        bolow7 = Sample.objects.filter(sensor=location, air_temperature_celsius__lt=7).values_list("capture_datetime_utc", "pk")
        months = Sample.objects.filter(sensor=location).dates('capture_datetime_utc', 'month')
        years = Sample.objects.filter(sensor=location).dates('capture_datetime_utc', 'year')
        for y in years:
            anualMax = Sample.objects.filter(sensor=location,capture_datetime_utc__year=y.year).aggregate(Max('air_temperature_celsius'))
            anualMin = Sample.objects.filter(sensor=location,capture_datetime_utc__year=y.year).aggregate(Min('air_temperature_celsius'))
            anualTemps.append([y.strftime('%Y'),anualMax['air_temperature_celsius__max'],anualMin['air_temperature_celsius__min']])
        for m in months:
            monthMax = Sample.objects.filter(sensor=location,capture_datetime_utc__month=m.month).aggregate(Max('air_temperature_celsius'))
            monthMin = Sample.objects.filter(sensor=location,capture_datetime_utc__month=m.month).aggregate(Min('air_temperature_celsius'))
            monthTemps.append([m.strftime('%Y'),m.strftime('%m'),monthMax['air_temperature_celsius__max'],monthMin['air_temperature_celsius__min']])
        for date, amount in bolow7:
            monthKey = date.month
            yearMonthKey = date.strftime('%Y-%m')
            yearKey = date.year
            nextYearKey = date.year + 1
            previousYearKey = date.year - 1
            if yearMonthKey in monthColdHours.keys():
                monthColdHours[yearMonthKey] += 0.25
            else:
                monthColdHours[yearMonthKey] = 0.25
            if monthKey > 9:
                key = str(yearKey)+'-'+str(nextYearKey)
                if key in anualColdHours.keys():
                    anualColdHours[key] += 0.25
                else:
                    anualColdHours[key] = 0.25
            if monthKey < 9:
                key = str(previousYearKey)+'-'+str(yearKey)
                if key in anualColdHours.keys():
                    anualColdHours[key] += 0.25
                else:
                    anualColdHours[key] = 0.25
        monthColdHours = collections.OrderedDict(sorted(monthColdHours.items()))
        anualColdHours = collections.OrderedDict(sorted(anualColdHours.items()))
    
        totalColdHours.append([location.plant_nickname,anualTemps,monthTemps,anualColdHours,monthColdHours])

    context = {'sensors':sensors,'totalColdHours':totalColdHours,'anualTemps':anualTemps,'monthTemps':monthTemps,'anualColdHours':anualColdHours,'coldHours':monthColdHours,'anualTemps':anualTemps}
    return render(request,'horasfrio.html', context)


def importEvap(request):
    output = ""
    i = 0
    page = requests.get('http://www.ipma.pt/pt/agrometeorologia/evapotranspiracao/index.jsp?page=index-geo.jsp')
    tree = html.fromstring(page.content)
    data = tree.xpath('//script/text()')[4]
    output = re.findall('et0\[0\][^;]*;', data)
    for item in output:
        a = re.findall('data":"[^"]*"', item)
        b = a[0].replace('data":"','').replace('"','')
        c = b.split(' ')
        dia = int(c[1])
        mes = getMonthNumber(c[2])
        ano = int(c[3])
        hora = int("14")
        capture_date = datetime(ano,mes,dia,hora)
        
        et = re.findall('JCOD":"a272","MEAN":[^:]*,', item)
        et = et[0].replace('JCOD":"a272","MEAN":','').replace(',','')
        et_obj, created = Evapotranspiration.objects.get_or_create(date = capture_date)
        et_obj.capture_date = capture_date.strftime("%Y-%m-%d %H:%M:%S")
        et_obj.value = et
        et_obj.save()
    
    #payload = {'success': True}
    #return HttpResponse(json.dumps(payload), content_type='application/json')
    return HttpResponse(et + ' - ' + str(capture_date) )
    

def getMonthNumber(monthName):
    months = dict(Jan=1, Fev=2, Mar=3, Abr=4, Mai=5, Jun=6, Jul=7, Ago=8, Set=9, Out=10, Nov=11, Dez=12)
    return months[monthName]
    

@login_required
def previsaotempo(request):
    return render(request,'previsaotempo.html')
    

    