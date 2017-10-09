#!/usr/bin/python
# -*- coding: latin-1 -*-
from django.core.management.base import BaseCommand, CommandError
from django.http import HttpResponse
from datetime import datetime, date
from fertilize.models import DayPortion, Culture, DayPortionProduct
from django.core import serializers
import json
from flowerpower.views import localtime
from tasks.models import Task, State
from fertilize.models import DayPortion, DayPortionProduct
from datetime import datetime, timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Command(BaseCommand):
        help = "Enviar Tarefas por email"
        
        def handle(self, *args, **options):
            
            days_timedelta = timedelta(days=7)
            tasksToSend = Task.objects.filter(startDate__lt=localtime()+days_timedelta).filter(state=State.objects.get(pk=1)) | Task.objects.filter(startDate__lt=localtime()+days_timedelta).filter(state=State.objects.get(pk=2))
            body = '<table border="0" style="border:solid 1px #f5f5f5" cellpadding="10" cellspacing="5" height="100%" width="100%"><thead><th style="background: rgba(219, 254, 77, 0.38);" colspan="5">TAREFAS</th></thead><thead style="background:#f5f5f5;"><th>Tarefa</th><th>Local</th><th>Categoria</th><th>Data</th><th>Descrição</th></thead>'
            for task in tasksToSend:
                body += '<tr style="border:solid 1px #f5f5f5; padding:5px; margin:0" >'
                body += '<td style="border:solid 1px #f5f5f5; background:#fff;">'
                body += str(task.name)
                body += '</td>'
                body += '<td style="border:solid 1px #f5f5f5; background:#fff;">'
                body += str(task.location)
                body += '</td>'
                body += '<td style="border:solid 1px #f5f5f5; background:#fff;">'
                body += str(task.category)
                body += '</td>'
                body += '<td style="border:solid 1px #f5f5f5; background:#fff;">'
                if (task.startDate != task.endDate):
                    body += str(task.startDate.strftime('%d-%m-%Y'))+' até '+str(task.endDate.strftime('%d-%m-%Y'))
                else:
                    body += str(task.startDate.strftime('%d-%m-%Y'))
                body += '</td>'
                body += '<td style="border:solid 1px #f5f5f5; background:#fff;">'
                body += str(task.description)
                body += '</td>'
                body += '</tr>'
            body += '</table>'
            fertilizesToSend = DayPortion.objects.filter(date__lt=localtime()+days_timedelta).filter(state=State.objects.get(pk=1)) | DayPortion.objects.filter(date__lt=localtime()+days_timedelta).filter(state=State.objects.get(pk=2))
            body += '<table border="0" style="border:solid 1px #f5f5f5" cellpadding="10" cellspacing="5" height="100%" width="100%"><thead><th style="background: rgba(77, 254, 213, 0.38);" colspan="5">Fertilizações</th></thead><thead style="background:#f5f5f5;"><th>Local</th><th>Período</th><th>Data</th><th>Descrição</th><th>Produtos Utilizados</th></thead>'
            for fertilize in fertilizesToSend:
                body += '<tr style="border:solid 1px #f5f5f5; padding:5px; margin:0" >'
                body += '<td style="border:solid 1px #f5f5f5; background:#fff;">'
                body += str(fertilize.irrigationSystem)
                body += '</td>'
                body += '<td style="border:solid 1px #f5f5f5; background:#fff;">'
                body += str(fertilize.period.period_name)
                body += '</td>'
                body += '<td style="border:solid 1px #f5f5f5; background:#fff;">'
                body += ''
                body += '</td>'
                body += '<td style="border:solid 1px #f5f5f5; background:#fff;">'
                body += '<p><strong>Água no depósito:</strong>'+str(fertilize.depositWaterUsed)+' L</p>'
                body += '<p><strong>Água Utilizada:</strong>'+str(fertilize.waterUsed)+' L</p>'
                body += '<p><strong>Tempo de Irrigação:</strong>'+str(fertilize.timeIrrigation)+' Minutos</p>'
                body += '<p><strong>Percentagem de Fertilização:</strong>'+str(fertilize.percentageFertilizer)+' %</p>'
                body += '<p><strong>Quantidade de Fertilização Utilizada:</strong>'+str(fertilize.fertilizer)+' L</p>'
                body += '<p><strong>EC:</strong>'+str(fertilize.ecIrrigation)+' uS/cm2</p>'
                body += '<p><strong>Disponível para fertilizar:</strong>'+str(fertilize.fertilizationTimes)+' Vezes</p>'
                body += '</td>'
                body += '<td style="border:solid 1px #f5f5f5; background:#fff;">'
                dayPortionProducts = DayPortionProduct.objects.filter(dayPortion=fertilize)
                for dayProduct in dayPortionProducts:
                    body += '<p><strong>'+str(dayProduct.product.name)+'</strong> - '+str(dayProduct.qt)+' Kg</p>'
                body += '</td>'
                body += '</tr>'
                body += '</table>'
            try:
                import smtplib
                from email.mime.multipart import MIMEMultipart
                from email.mime.text import MIMEText

                gmail_user = 'vitaminasdobosque@gmail.com'
                gmail_pwd = 'vita#2016'
                FROM = 'vitaminasdobosque@gmail.com'
                TO = ['sfaraujo@gmail.com,georgefaraujo@gmail.com']
                tasksDate = localtime()+days_timedelta
                SUBJECT = "Tarefas até "+str(tasksDate.strftime('%d-%m-%Y'))
                BODY = body

                MESSAGE = MIMEMultipart('alternative')
                MESSAGE['subject'] = SUBJECT
                MESSAGE['To'] = ", ".join(TO)
                MESSAGE['From'] = FROM
                MESSAGE.preamble = """ """
         
                # Record the MIME type text/html.
                HTML_BODY = MIMEText(BODY, 'html')
                
                # Attach parts into message container.
                # According to RFC 2046, the last part of a multipart message, in this case
                # the HTML message, is best and preferred.
                MESSAGE.attach(HTML_BODY)
                
                # Prepare actual message
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, MESSAGE.as_string())
                server.close()
                return "Email enviado com sucesso"
            except:
                return "Falha no envio de email"