from django.core.management.base import BaseCommand, CommandError
from flowerpower.models import Evapotranspiration
from flowerpower.views import getMonthNumber
import requests
from lxml import html
import re
from pprint import pformat
from datetime import datetime
import xml.etree.ElementTree as ET
import pytz
local = pytz.timezone("Europe/Lisbon")

class Command(BaseCommand):
        help = "Importar EVap ET0"
        
        def handle(self, *args, **options):
            
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
                capture_date = datetime(ano,mes,dia,hora,tzinfo=pytz.UTC)
                
                et = re.findall('JCOD":"a272","MEAN":[^:]*,', item)
                et = et[0].replace('JCOD":"a272","MEAN":','').replace(',','')
                et_obj, created = Evapotranspiration.objects.get_or_create(date = capture_date)
                et_obj.capture_date = capture_date.strftime("%Y-%m-%d %H:%M:%S")
                et_obj.value = et
                et_obj.save()