from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'importdata/$', views.importData, name='importData'),
    url(r'importevap/$', views.importEvap, name='importEvap'),
    url(r'previsaotempo/$', views.previsaotempo, name='previsaotempo'),
    url(r'evapotranspiracao/$', views.evapotranspiracao, name='evapotranspiracao'),
    url(r'temperaturas/$', views.temperaturas, name='temperaturas'),
    url(r'sensores/(?P<sensor_id>\d+)/(?P<date>\d+)$', views.sensor, name='sensor'),
    url(r'configsensors/$', views.configSensors, name='configSensors'),
    url(r'usergroups/$', views.userGroups, name='userGroups'),
    url(r'parrotaccount/$', views.parrotAccount, name='parrotAccount'),

]