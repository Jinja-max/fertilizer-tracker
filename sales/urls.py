from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('all-details/',views.all_details, name="all_details"),
]