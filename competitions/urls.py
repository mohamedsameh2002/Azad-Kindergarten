from django.urls import path
from . import views

app_name = "competition"

urlpatterns = [

path('',views.competitions,name='competitions')
]
