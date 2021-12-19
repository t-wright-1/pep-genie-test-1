from django.urls import path
from . import views

app_name = 'lab'

urlpatterns = [
    path('resources',views.resources, name = 'resources'),
    path('sequence_studies',views.sequence_studies, name = 'sequence_studies'),
    path('ss_result',views.ss_result, name = 'ss_result'),
]