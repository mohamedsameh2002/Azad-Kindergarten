from django.urls import path
from . import views

app_name = "homework"

urlpatterns = [
path("get/<str:year>/", views.get_homework,name='get'),
path("add-homework/", views.add_homework,name='add-homework'),
]
