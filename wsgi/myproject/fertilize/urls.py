from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'fertilizacao/culturas/$', views.cultures, name='cultures'),
    url(r'fertilizacao/culturas/(?P<culture_id>\d+)/ano/(?P<year>\d+)/$', views.fertilization, name='fertilization'),
    url(r'fertilizacao/culturas/(?P<culture_id>\d+)/ano/(?P<year>\d+)/periodo/(?P<period_id>\d+)$', views.period, name='period'),
    url(r'fertilizacao/culturas/(?P<culture_id>\d+)/ano/(?P<year>\d+)/periodo/(?P<period_id>\d+)/agenda/$', views.calendar, name='calendar'),
    url(r'fertilizacao/culturas/(?P<id>\d+)/apagar$', views.culturedelete, name='culturedelete'),
    url(r'fertilizacao/culturas/(?P<culture_id>\d+)/periodo/novo$', views.newPeriod, name='newPeriod'),
    url(r'fertilizacao/culturas/(?P<culture_id>\d+)/periodo/atualizar$', views.updatePeriod, name='updatePeriod'),
    url(r'fertilizacao/culturas/periodo/(?P<id>\d+)/apagar$', views.perioddelete, name='perioddelete'),
    url(r'fertilizacao/getcultureneed/(?P<culture_id>\d+)/ano/(?P<year>\d+)$', views.getCultureNeed, name='getCultureNeed'),
    url(r'fertilizacao/setcultureneed/(?P<period_id>\d+)/$', views.setCultureNeed, name='setCultureNeed'),
    url(r'fertilizacao/getfieldneed/(?P<culture_id>\d+)/ano/(?P<year>\d+)$', views.getFieldNeed, name='getFieldNeed'),
    url(r'fertilizacao/getestimateqty/(?P<culture_id>\d+)/ano/(?P<year>\d+)$', views.getEstimateQty, name='getEstimateQty'),
    url(r'fertilizacao/culturas/periodo/necessidade/apagar', views.deleteFieldNeedProduct, name='deleteFieldNeedProduct'),
    url(r'fertilizacao/culturas/periodo/produto/apagar', views.deleteProduct, name='deleteproduct'),
    url(r'fertilizacao/culturas/(?P<culture_id>\d+)/periodo/(?P<period_id>\d+)/agenda/novodia$', views.createDayPortion, name='createDayPortion'),
    url(r'fertilizacao/culturas/(?P<culture_id>\d+)/periodo/(?P<period_id>\d+)/agenda/apagardia$', views.deleteDayPortion, name='deleteDayPortion'),
    url(r'fertilizacao/culturas/(?P<culture_id>\d+)/periodo/(?P<period_id>\d+)/agenda/novoprodutodia$', views.addDayPortionProduct, name='addDayPortionProduct'),
    url(r'fertilizacao/culturas/(?P<culture_id>\d+)/periodo/(?P<period_id>\d+)/agenda/atualizardia$', views.updateDayPortion, name='updateDayPortion'),
    url(r'fertilizacao/(?P<culture_id>\d+)/(?P<year>\d+)$', views.allFertilizations, name='allFertilizations'),
]