from django.urls import path

from .views import *

urlpatterns = [
    path('', Schemas.as_view(), name='schemas'),
    path('<str:name>', OneSchemas.as_view(), name='schemas'),
    path('edit/<str:name>', EditScheme.as_view(), name='edit_scheme'),
    path('delete/<str:name>', DeleteScheme.as_view(), name='delete_scheme'),
]