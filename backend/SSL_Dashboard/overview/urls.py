from django.urls import path
from . import views

urlpatterns = [
    path('data/', views.overview_data, name='overview_data'),
]
