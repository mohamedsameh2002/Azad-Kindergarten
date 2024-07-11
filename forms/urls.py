from django.urls import path
from . import views

app_name = "forms"

urlpatterns = [
path("register/", views.registration_in_school,name='register'),
]
