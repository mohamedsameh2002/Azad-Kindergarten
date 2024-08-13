from django.contrib import admin
from .models import *
# Register your models here.

class TeacherAdmin (admin.ModelAdmin):
    list_display=['name','number']
    
admin.site.register(Homework)
admin.site.register(Years)
admin.site.register(Teacher,TeacherAdmin)
