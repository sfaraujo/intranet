from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'tarefas/$', views.tasks, name='tasks'),
    url(r'tarefas/getTasks/', views.getTasks, name='getTasks'),
    url(r'tarefas/savetask$', views.saveTask, name='saveTask'),
    url(r'tarefas/deletetask$', views.deleteTask, name='deleteTask'),
    url(r'tarefas/saveWorkDay$', views.saveWorkDay, name='saveWorkDay'),
    url(r'tarefas/deleteWorkDay$', views.deleteWorkDay, name='deleteWorkDay'),
    

]