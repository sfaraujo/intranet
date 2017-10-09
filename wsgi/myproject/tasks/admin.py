from django.contrib import admin
from .models import *

admin.site.register(Task)
admin.site.register(TaskCategory)
admin.site.register(State)
admin.site.register(Local)
admin.site.register(WorkDay)

