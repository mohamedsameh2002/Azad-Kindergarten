from django.urls import path
from . import views

app_name = "competition"

urlpatterns = [
path("register/", views.registration_in_school,name='register'),
]
