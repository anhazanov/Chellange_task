from django.urls import path

from .views import *


urlpatterns = [
    path('generate_data', generate_data, name='generate_data'),
]