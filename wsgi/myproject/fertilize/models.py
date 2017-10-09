from __future__ import unicode_literals

from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User, Group
from tasks.models import State
import json

class Product(models.Model):
    name = models.CharField(db_index=True, max_length=255,)
    supplier = models.CharField(max_length=255, blank=True)
    scientific_name = models.CharField(max_length=255,)
    nno3 = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True,)
    nnh4 = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    p = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    k = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    ca = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    mg = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    sso4 = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    b = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    cu = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    fe = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    mn = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    mo = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    zn = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    ec = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    solubility = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    ph = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    price_per_kilo = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    
    def __unicode__(self):
    	return unicode(self.name)
    
    

class Culture(models.Model):
    name = models.CharField(db_index=True, max_length=255,)
    area = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True)
    group = models.ForeignKey(Group, null=True, blank=True)
    def __unicode__(self):
        	return unicode(self.name)
    """"
    def save(self, *args, **kwargs):
        super(Culture, self).save(*args, **kwargs)
        fields = CultureNeed.objects.filter(culture = self.pk)
        for field in fields:
            field.save()
    """
    
class Period(models.Model):
    culture = models.ForeignKey(Culture, null=True, blank=True)
    period_name = models.CharField(db_index=True, max_length=255,)
    days = models.DurationField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    year = models.CharField(max_length=255, blank=True)

    """"
    def save(self, *args, **kwargs):

        self.year = self.start_date.year
        print self.year

        super(Period, self).save(*args, **kwargs)
    """
       
    def natural_key(self):
        return unicode(self.period_name)
        
    def __unicode__(self):
    	return unicode(self.culture) + ' - ' + unicode(self.days) + ' - ' + unicode(self.period_name)
    

class CultureNeed(models.Model):
    period = models.ForeignKey(Period, null=True, blank=True)
    nno3 = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    nnh4 = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    p = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    k = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    ca = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    mg = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    sso4 = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    b = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    cu = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    fe = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    mn = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    mo = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    zn = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    
    def __unicode__(self):
    	return unicode(self.period)
    	
    def natural_key(self):
        return (self.pk,) + self.period.natural_key()

    def save(self, *args, **kwargs):
        fieldNeed, created = FieldNeed.objects.get_or_create(period = self.period)
        fieldNeed.nno3 = float(self.nno3) * float((self.period.culture.area/10000))
        fieldNeed.nnh4 = float(self.nnh4) * float((self.period.culture.area/10000))
        fieldNeed.p = float(self.p) * float((self.period.culture.area/10000))
        fieldNeed.k = float(self.k) * float((self.period.culture.area/10000))
        fieldNeed.ca = float(self.ca) * float((self.period.culture.area/10000))
        fieldNeed.mg = float(self.mg) * float((self.period.culture.area/10000))
        fieldNeed.sso4 = float(self.sso4) * float((self.period.culture.area/10000))
        fieldNeed.b = float(self.b) * float((self.period.culture.area/10000))
        fieldNeed.cu = float(self.cu) * float((self.period.culture.area/10000))
        fieldNeed.fe = float(self.fe) * float((self.period.culture.area/10000))
        fieldNeed.mn = float(self.mn) * float((self.period.culture.area/10000))
        fieldNeed.mo = float(self.mo) * float((self.period.culture.area/10000))
        fieldNeed.zn = float(self.zn) * float((self.period.culture.area/10000))
        fieldNeed.save()
        super(CultureNeed, self).save(*args, **kwargs)

class FieldNeed(models.Model):
    period = models.ForeignKey(Period, null=True, blank=True)
    nno3 = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    nnh4 = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    p = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    k = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    ca = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    mg = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    sso4 = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    b = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    cu = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    fe = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    mn = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    mo = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    zn = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    
    def __unicode__(self):
    	return unicode(self.period)
    

class FieldNeedProducts(models.Model):
    period = models.ForeignKey(Period, null=True, blank=True)
    product = models.ForeignKey(Product, null=True, blank=True)
    qt = models.DecimalField(max_digits=10, decimal_places=3, default='0', blank=True)
    qtAppliedSum = models.DecimalField(max_digits=10, decimal_places=3, default='0', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    def __unicode__(self):
        return unicode(self.period) + ' - ' + unicode(self.product) + ' - ' + unicode(self.qt) + ' - ' + unicode(self.price)


class FieldProductSum(models.Model):
    period = models.ForeignKey(Period, null=True, blank=True)
    nno3 = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    nnh4 = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    p = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    k = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    ca = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    mg = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    sso4 = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    b = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    cu = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    fe = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    mn = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    mo = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    zn = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, default='0', blank=True)
    
    def __unicode__(self):
    	return unicode(self.period)


class IrrigationSystem(models.Model):
    culture = models.ForeignKey(Culture, null=True, blank=True)
    waterPerHour = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    fertilizerPerHour = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    #depositCapacity = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True)

    def __unicode__(self):
        	return unicode(self.culture)


    

class DayPortion(models.Model):
    period = models.ForeignKey(Period, null=True, blank=True)
    date = models.DateField(db_index=True, null=True, blank=True)
    irrigationSystem = models.ForeignKey(IrrigationSystem, null=True, blank=True)
    depositWaterUsed = models.DecimalField(max_digits=5, decimal_places=0, default='1', null=True, blank=True)
    waterUsed = models.DecimalField(max_digits=5, decimal_places=0, default='1', null=True, blank=True)
    timeIrrigation = models.DecimalField(max_digits=10, decimal_places=2, default='1', null=True, blank=True)
    percentageFertilizer = models.DecimalField(max_digits=3, decimal_places=0, default='100', null=True, blank=True)
    fertilizerPerHour = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    fertilizer = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    ecIrrigation = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    fertilizationTimes = models.DecimalField(max_digits=3, decimal_places=0, null=True, blank=True)
    state = models.ForeignKey(State, null=True, blank=True)
    #state = models.CharField(max_length=255,)
    def __unicode__(self):
        return unicode(self.period) + ' - ' + unicode(self.date)
        
class DayPortionProduct(models.Model):
    dayPortion = models.ForeignKey(DayPortion, null=True, blank=True)
    product = models.ForeignKey(Product, null=True, blank=True)
    qt = models.DecimalField(max_digits=10, decimal_places=3, default='0', blank=True)

    def __unicode__(self):
        return unicode(self.dayPortion) + ' - ' + unicode(self.product) + ' - ' + unicode(self.qt)
        
    
    def get_json(self):
        return {
            'id': self.dayPortion.id,
            'period': str(self.dayPortion.period),
            'date': str(self.dayPortion.date),
            'product': str(self.product),
            'qt': float(self.qt),
             }