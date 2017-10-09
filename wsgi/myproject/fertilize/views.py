from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.core import serializers
from forms import *
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from decimal import *
from flowerpower.models import Sensor
from django.contrib.auth.models import User, Group

@login_required
def fertilization(request, *args, **kwargs):
    culture_id = kwargs.get('culture_id')
    culture = Culture.objects.get(pk=culture_id)
    sensors = []
    if request.user.is_superuser:
        sensors = Sensor.objects.all()
    else:
        groups = Group.objects.filter(user=request.user)
        for group in groups:
            sensors += Sensor.objects.filter(group=group)
    year = kwargs.get('year')
    periods = Period.objects.filter(culture=culture_id, year=year)

    if request.method == 'POST':
        alldata=request.POST
        product = Product.objects.get(pk=alldata.get("product", "0"))
        period = Period.objects.get(pk=alldata.get("period", "0"))
        form_obj, created = FieldNeedProducts.objects.get_or_create(product=product,period=period)
        form_obj.qt = float(alldata.get("qt", "0"))
        form_obj.price = float(alldata.get("qt", "0")) * float(product.price_per_kilo)
        form_obj.save()
        getTotalFieldNeed(request, period_id=period.pk)
        return redirect('fertilization', culture_id=period.culture.pk)
        
    context = {'year':year,'culture' : culture,'periods':periods, 'products' : Product.objects.all(), 'cultures' : Culture.objects.all(),'sensors':sensors}
    return render(request,'fertilization.html', context)

def deleteFieldNeedProduct(request):
    id = request.GET.get('id', '')
    fieldNeedProduct = FieldNeedProducts.objects.get(pk = id)
    fieldNeedProduct.delete()
    getTotalFieldNeed(request, period_id=fieldNeedProduct.period.pk)
    payload = {'success': True}
    return HttpResponse(json.dumps(payload), content_type='application/json')
    
    
def getTotalFieldNeed(request, **kwargs):
    culture_id = kwargs.get('culture_id')
    period_id = kwargs.get('period_id')
    periods = Period.objects.filter(pk=period_id)
    nno3=nnh4=p=k=ca=mg=sso4=b=cu=fe=mn=mo=zn=total_price = 0
    for period in periods:
        fieldNeedProducts = FieldNeedProducts.objects.filter(period=period)
        for fieldNeedProduct in fieldNeedProducts:
            nno3 += fieldNeedProduct.product.nno3 * fieldNeedProduct.qt
            nnh4 += fieldNeedProduct.product.nnh4 * fieldNeedProduct.qt
            p += fieldNeedProduct.product.p * fieldNeedProduct.qt
            k += fieldNeedProduct.product.k * fieldNeedProduct.qt
            ca += fieldNeedProduct.product.ca * fieldNeedProduct.qt
            mg += fieldNeedProduct.product.mg * fieldNeedProduct.qt
            sso4 += fieldNeedProduct.product.sso4 * fieldNeedProduct.qt
            b += fieldNeedProduct.product.b * fieldNeedProduct.qt
            cu += fieldNeedProduct.product.cu * fieldNeedProduct.qt
            fe += fieldNeedProduct.product.fe * fieldNeedProduct.qt
            mn += fieldNeedProduct.product.mn * fieldNeedProduct.qt
            mo += fieldNeedProduct.product.mo * fieldNeedProduct.qt
            zn += fieldNeedProduct.product.zn * fieldNeedProduct.qt
            total_price += fieldNeedProduct.price
            
        fieldsum, created = FieldProductSum.objects.get_or_create(period=period)
        fieldsum.nno3 = nno3
        fieldsum.nnh4 = nnh4
        fieldsum.p = p
        fieldsum.k = k
        fieldsum.ca = ca
        fieldsum.mg = mg
        fieldsum.sso4 = sso4
        fieldsum.b = b
        fieldsum.cu = cu
        fieldsum.fe = fe
        fieldsum.mn = mn
        fieldsum.mo = mo
        fieldsum.zn = zn
        fieldsum.total_price = total_price
        fieldsum.save()

    return True

@login_required
def getCultureNeed(request, **kwargs):
    cultureNeed = []
    culture_id = kwargs.get('culture_id')
    year = kwargs.get('year')
    periods = Period.objects.filter(culture=Culture.objects.get(pk=culture_id), year=year)
    for period in periods:
        cultureNeed += CultureNeed.objects.filter(period=period)
    data = serializers.serialize('json', cultureNeed, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
@login_required
def setCultureNeed(request, **kwargs):
    period_id = kwargs.get('period_id')
    period = Period.objects.get(pk=period_id)
    if request.method == 'POST':
        alldata=request.POST
        form_obj, created = CultureNeed.objects.get_or_create(period=period)
        form_obj.nno3 = float(alldata.get("nno3", "0").replace(',',''))
        form_obj.nnh4 = float(alldata.get("nnh4", "0").replace(',',''))
        form_obj.p = float(alldata.get("p", "0").replace(',',''))
        form_obj.k = float(alldata.get("k", "0").replace(',',''))
        form_obj.ca = float(alldata.get("ca", "0").replace(',',''))
        form_obj.mg = float(alldata.get("mg", "0").replace(',',''))
        form_obj.sso4 = float(alldata.get("sso4", "0").replace(',',''))
        form_obj.b = float(alldata.get("b", "0").replace(',',''))
        form_obj.cu = float(alldata.get("cu", "0").replace(',',''))
        form_obj.f = float(alldata.get("f", "0").replace(',',''))
        form_obj.mn = float(alldata.get("mn", "0").replace(',',''))
        form_obj.mo = float(alldata.get("mo", "0").replace(',',''))
        form_obj.zn = float(alldata.get("zn", "0").replace(',',''))
        form_obj.save()
        payload = {'success': True}
        return HttpResponse(json.dumps(payload), content_type='application/json')
    return redirect('fertilization', culture_id=period.culture.pk)

@login_required
def getFieldNeed(request, **kwargs):
    fieldNeed = []
    culture_id = kwargs.get('culture_id')
    year = kwargs.get('year')
    periods = Period.objects.filter(culture=Culture.objects.get(pk=culture_id),year=year)
    for period in periods:
        fieldNeed += FieldNeed.objects.filter(period=period)
    data = serializers.serialize('json', fieldNeed, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return HttpResponse(data, content_type='application/json')

@login_required
def getEstimateQty(request, **kwargs):
    estimateQty = []
    culture_id = kwargs.get('culture_id')
    year = kwargs.get('year')
    periods = Period.objects.filter(culture=Culture.objects.get(pk=culture_id),year=year)
    for period in periods:
        estimateQty += FieldProductSum.objects.filter(period=period)
    data = serializers.serialize('json', estimateQty, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return HttpResponse(data, content_type='application/json')
    

@csrf_exempt
@login_required
def cultures(request):
    cultures = []
    periods = []
    groups = Group.objects.filter(user=request.user)
    for group in groups:
        cultures += Culture.objects.filter(group=group)
    for culture in cultures:
        periods += Period.objects.filter(culture=culture.pk)
    if request.method == 'POST':
        alldata=request.POST
        name = alldata.get("name", "0")
        area = alldata.get("area", "0")
        group = Group.objects.get(pk=alldata.get("group", "0"))
        form_obj, created = Culture.objects.get_or_create(name=name,group=group)
        form_obj.area = area
        form_obj.save()
        return redirect('cultures')
    context = {'periods':periods,'cultures' : cultures,'groups' : groups}
    return render(request,'cultures.html', context)


def culturedelete(request, id):    
    culture = Culture.objects.get(pk = id)
    culture.delete()
    payload = {'success': True}
    return HttpResponse(json.dumps(payload), content_type='application/json')


@csrf_exempt
@login_required
def newPeriod(request, **kwargs):
    culture_id = kwargs.get('culture_id')
    if request.method == 'POST':
        alldata=request.POST
        form_obj = Period.objects.create(culture=Culture.objects.get(pk=culture_id))
        form_obj.period_name = alldata.get("period_name", "0")
        form_obj.start_date = alldata.get("start_date", "0")
        form_obj.end_date = alldata.get("end_date", "0")
        start = datetime.strptime(form_obj.start_date, '%Y-%m-%d')
        end = datetime.strptime(form_obj.end_date, '%Y-%m-%d')
        form_obj.days = end - start
        form_obj.year = start.year
        form_obj.save()
        cultureNeed, created = CultureNeed.objects.get_or_create(period = form_obj)
        payload = {'success': True}
        return HttpResponse(json.dumps(payload), content_type='application/json')
    return redirect('fertilization', culture_id=culture_id)
    

@csrf_exempt
@login_required
def updatePeriod(request, **kwargs):
    culture_id = kwargs.get('culture_id')
    if request.method == 'POST':
        alldata=request.POST
        form_obj = Period.objects.get(pk = alldata.get("pk", "0"), culture=Culture.objects.get(pk=culture_id))
        form_obj.period_name = alldata.get("period_name", "0")
        form_obj.start_date = alldata.get("start_date", "0")
        form_obj.end_date = alldata.get("end_date", "0")
        start = datetime.strptime(form_obj.start_date, '%Y-%m-%d')
        end = datetime.strptime(form_obj.end_date, '%Y-%m-%d')
        form_obj.days = end - start
        form_obj.year = start.year
        form_obj.save()
        cultureNeed, created = CultureNeed.objects.get_or_create(period = form_obj)
        payload = {'success': True}
        return HttpResponse(json.dumps(payload), content_type='application/json')
    return redirect('fertilization', culture_id=culture_id)

@login_required
def perioddelete(request, id):    
    period = Period.objects.get(pk = id)
    period.delete()
    payload = {'success': True}
    return HttpResponse(json.dumps(payload), content_type='application/json')


@login_required
def period(request, *args, **kwargs):
    culture_id = kwargs.get('culture_id')
    sensors = []
    if request.user.is_superuser:
        sensors = Sensor.objects.all()
    else:
        groups = Group.objects.filter(user=request.user)
        for group in groups:
            sensors += Sensor.objects.filter(group=group)
    period_id = kwargs.get('period_id')
    year = kwargs.get('year')
    culture = Culture.objects.get(pk=culture_id)
    periods = Period.objects.filter(culture=culture_id, year=year)
    period = Period.objects.get(pk=period_id)
    fieldNeed = FieldNeed.objects.get(period=period)
    try:
        fieldProductSum = FieldProductSum.objects.get(period=period)
    except:
        fieldProductSum = None
    fieldNeedProducts = FieldNeedProducts.objects.filter(period=period)
    
    if request.method == 'POST':
        alldata=request.POST
        product = Product.objects.get(pk=alldata.get("product", "0"))
        form_obj, created = FieldNeedProducts.objects.get_or_create(product=product,period=period)
        form_obj.qt = float(alldata.get("qt", "0"))
        form_obj.price = float(alldata.get("qt", "0")) * float(product.price_per_kilo)
        form_obj.save()
        getTotalFieldNeed(request, period_id=period.pk)
        return redirect('period', culture_id=period.culture.pk, period_id=period_id, year=year)

        
    context = {'year':year,'culture' : culture, 'period': period, 'periods': periods, 'fieldNeed': fieldNeed, 'fieldProductSum': fieldProductSum,'products' : Product.objects.all(), 'fieldNeedProducts': fieldNeedProducts,'cultures' : Culture.objects.all(),'sensors':sensors}
    return render(request,'period.html', context)


@login_required
def calendar(request, *args, **kwargs):
    culture_id = kwargs.get('culture_id')
    sensors = []
    if request.user.is_superuser:
        sensors = Sensor.objects.all()
    else:
        groups = Group.objects.filter(user=request.user)
        for group in groups:
            sensors += Sensor.objects.filter(group=group)
    period_id = kwargs.get('period_id')
    year = kwargs.get('year')
    culture = Culture.objects.get(pk=culture_id)
    periods = Period.objects.filter(culture=culture_id)
    period = Period.objects.get(pk=period_id)
    states = State.objects.all()
    fieldNeedProducts = FieldNeedProducts.objects.filter(period=period)
    irrigationSystem = IrrigationSystem.objects.get(culture=culture_id)
    delta = period.end_date - period.start_date
    loop_days = range(1, delta.days)
    dates = []
    for i in range(0,delta.days): 
        dates += [period.start_date + timedelta(days=i)]
    
    context = {'states':states,'year':year,'dates':dates,'culture' : culture, 'period': period, 'periods': periods, 'fieldNeedProducts': fieldNeedProducts,'cultures' : Culture.objects.all(),'sensors':sensors}
    return render(request,'calendar.html', context)

@login_required
def createDayPortion(request, *args, **kwargs):
    if request.method == 'POST':
        alldata=request.POST
        date = alldata.get("date", "0")
        culture_id = kwargs.get('culture_id')
        period_id = kwargs.get('period_id')
        culture = Culture.objects.get(pk=culture_id)
        period = Period.objects.get(pk=period_id)
        irrigationSystem = IrrigationSystem.objects.get(culture=culture)
        dayPortion_obj, created = DayPortion.objects.get_or_create(period=period, date=date, irrigationSystem=irrigationSystem, state=State.objects.get(pk=1))
        payload = {'success': True}
        return HttpResponse(json.dumps(payload), content_type='application/json')


@login_required
def updateDayPortion(request, *args, **kwargs):
    culture_id = kwargs.get('culture_id')
    period_id = kwargs.get('period_id')
    culture = Culture.objects.get(pk=culture_id)
    period = Period.objects.get(pk=period_id)
    irrigationSystem = IrrigationSystem.objects.get(culture=culture_id)
    if request.method == 'POST':
        alldata=request.POST
        print alldata
        date = alldata.get("date", "0")
        fertilizerPerHour = alldata.get("fertilizerPerHour", "0")
        timeIrrigation = alldata.get("timeIrrigation", "0")
        depositWaterUsed = alldata.get("depositWaterUsed", "0")
        percentageFertilizer = alldata.get("percentageFertilizer", "0")
        state = alldata.get("state", "0")
        form_obj = DayPortion.objects.get(period = period, date=date)
        form_obj.timeIrrigation = Decimal(timeIrrigation)
        form_obj.fertilizerPerHour = Decimal(fertilizerPerHour)
        form_obj.depositWaterUsed = Decimal(depositWaterUsed)
        form_obj.percentageFertilizer = Decimal(percentageFertilizer)
        form_obj.save()

        waterUsed = Decimal(irrigationSystem.waterPerHour)*(Decimal(timeIrrigation)/60)
        form_obj.waterUsed = waterUsed
        fertilizer = (Decimal(percentageFertilizer)/100)*Decimal(fertilizerPerHour)*Decimal(timeIrrigation)/60
        form_obj.fertilizer = fertilizer
        form_obj.save()
        
        dayPortionProducts = DayPortionProduct.objects.filter(dayPortion=form_obj)
        qtTotal = 0
        for dayPortionProduct in dayPortionProducts.all():
            qtTotal += dayPortionProduct.qt*1000
        depositConcentration = Decimal(qtTotal)/Decimal(depositWaterUsed)
        fertilizePerIrrigation = depositConcentration*((Decimal(percentageFertilizer)/100)*Decimal(fertilizerPerHour)*Decimal(timeIrrigation)/60)
        irrigationConcentration = Decimal(fertilizePerIrrigation)/Decimal(waterUsed)
        productec = 0
        for dayPortionProduct in dayPortionProducts.all():
            productPercentage = (dayPortionProduct.qt*1000 / qtTotal)
            productec += Decimal(productPercentage)*Decimal(dayPortionProduct.product.ec)
        finalEC = irrigationConcentration*productec
        form_obj.ecIrrigation = finalEC
        form_obj.fertilizationTimes = Decimal(depositWaterUsed)/Decimal(fertilizer)
        form_obj.state = State.objects.get(pk=state)
        form_obj.save()

        
        payload = {'success': True,'state':state}
        return HttpResponse(json.dumps(payload), content_type='application/json')


@login_required
def addDayPortionProduct(request, *args, **kwargs):
    if request.method == 'POST':
        alldata=request.POST
        period = Period.objects.get(pk=kwargs.get('period_id'))
        dayPortion = alldata.get("dayPortion", "0")
        productPk = alldata.get("product", "0")
        productQt = Decimal(alldata.get("qt", "0"))
        dayPortionProduct_obj, created = DayPortionProduct.objects.get_or_create(dayPortion=DayPortion.objects.get(pk=dayPortion), product=Product.objects.get(pk=productPk))
        fieldNeedProduct = FieldNeedProducts.objects.get(period= period, product=Product.objects.get(pk=productPk))
        if created == False:
            fieldNeedProduct.qtAppliedSum += productQt-dayPortionProduct_obj.qt
        else:
            fieldNeedProduct.qtAppliedSum += productQt
        fieldNeedProduct.save()
        dayPortionProduct_obj.qt=productQt
        dayPortionProduct_obj.save()
        payload = {'success': True}
        return HttpResponse(json.dumps(payload), content_type='application/json')

        
@login_required
def deleteDayPortion(request, *args, **kwargs):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        dayPortion_obj = DayPortion.objects.get(pk=id)
        dayPortion_obj.delete()
        payload = {'success': True}
        return HttpResponse(json.dumps(payload), content_type='application/json')


@login_required
def deleteProduct(request):
    id = request.GET.get('id', '')
    productid = request.GET.get('productid', '')
    dayPortionProduct = DayPortionProduct.objects.get(pk=id)
    fieldNeedProduct = FieldNeedProducts.objects.get(period=dayPortionProduct.dayPortion.period, product=Product.objects.get(pk=productid))
    fieldNeedProduct.qtAppliedSum = fieldNeedProduct.qtAppliedSum - dayPortionProduct.qt
    fieldNeedProduct.save()
    dayPortionProduct.delete()
    payload = {'success': True}
    return HttpResponse(json.dumps(payload), content_type='application/json')


@login_required
def allFertilizations(request, *args, **kwargs):
    culture_id = kwargs.get('culture_id')
    year = kwargs.get('year')
    try:
        culture = Culture.objects.get(pk=culture_id)
        periods = Period.objects.filter(culture=culture, year=year)
    except:
        culture = None
        periods = Period.objects.filter(year=year)
    dayPortions = DayPortion.objects.filter(period__in = periods)
    context = {'dayPortions':dayPortions,'year':year,'culture' : culture,'periods':periods, 'products' : Product.objects.all(), 'cultures' : Culture.objects.all()}
    return render(request,'allFertilizations.html', context)
    
    
