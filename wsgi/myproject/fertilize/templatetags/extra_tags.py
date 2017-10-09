from django import template
from ..models import *
from tasks.models import *
from flowerpower.models import Sample, Location
register = template.Library()
import json
from datetime import datetime, timedelta
from django.utils import timezone
import pytz, datetime
local = pytz.timezone("Europe/Lisbon")

   
@register.filter
def getfieldNeedProducts(request, period_id):
    try:
        return FieldNeedProducts.objects.filter(period = Period.objects.get(pk=period_id))
    except:
        return None

@register.filter
def getPeriodsByCulture(request):
    try:
        return Period.objects.filter(culture = request)
    except:
        return None
        
@register.filter
def getCultureNeedByPeriod(value):
    try:
        return CultureNeed.objects.get(period = value)
    except:
        return None
        
@register.filter
def getPeriodName(value):
    try:
        period = Period.objects.get(pk = value)
        return period.period_name
    except:
        return None
        
@register.filter
def subtract(value, arg):
    return value - arg
    

@register.filter
def getdayPortion(request, date):
    try:
        return DayPortion.objects.get(period = request, date = date)
    except:
        return None

@register.filter
def getdayPortionProducts(value):
    try:
        return DayPortionProduct.objects.filter(dayPortion = value)
    except:
        return None
        
@register.filter
def getYearsByCulture(value):
    dates = Period.objects.filter(culture=value).dates('start_date','year',order='DESC')
    years = []
    for date in dates:
        years += [date.year]
    return years
    
@register.filter
def getPeriodsByYear(request, year):
    periods = Period.objects.filter(culture=request, year=year).order_by('start_date')
    return periods
    
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
    

@register.filter
def durationByCategory(request,culture):
    duration = {}
    years = Task.objects.all().dates('startDate', 'year')
    for year in years:
        tasks = Task.objects.filter(category=request, location=culture, startDate__year=year.year)
        for task in tasks:
            try:
                duration[year.year] += task.duration
            except:
                duration[year.year] = task.duration
    return duration
    

@register.filter
def getWorkDaysByTasks(request):
    workdays = WorkDay.objects.filter(task=request)
    return workdays
    
@register.filter
def getWorkDaysByTasksJSON(request):
    workdays = WorkDay.objects.filter(task=request)
    return json.dumps(workdays)
    



@register.filter
def getSoilSampleBefore(value):
    date = value.date
    culture = str(value.period.culture)[:5]
    try:
        location = Location.objects.filter(plant_nickname__icontains = culture).first()
        sample = Sample.objects.filter(sensor = location, capture_datetime_utc__year = date.year, capture_datetime_utc__month = date.month, capture_datetime_utc__day = date.day).first()
        return sample
    except:
        return None
        
@register.filter
def getSoilSampleAfter(value):
    date = value.date
    next_date = date + timedelta(days=1)
    culture = str(value.period.culture)[:5]
    try:
        location = Location.objects.filter(plant_nickname__icontains = culture).first()
        sample = Sample.objects.filter(sensor = location, capture_datetime_utc__year = next_date.year, capture_datetime_utc__month = next_date.month, capture_datetime_utc__day = next_date.day).first()
        return sample
    except:
        return None
        

@register.filter
def getPumpPercentage(value):
    
    percentage = (value.fertilizerPerHour * 100)/250
    return percentage
    
