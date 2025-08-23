from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('all-details/',views.all_details, name="all_details"),
    # Add this to urlpatterns list in sales/urls.py:
    path('enter-old-data/', views.enter_old_data, name='enter_old_data'),
]