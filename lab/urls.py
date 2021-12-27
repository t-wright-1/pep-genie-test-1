from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'lab'

urlpatterns = [
    path('resources',views.resources, name = 'resources'),
    path('sequence_studies',views.sequence_studies, name = 'sequence_studies'),
    path('ss_result',views.ss_result, name = 'ss_result'),
    path('formatter',views.formatter, name = 'formatter'),
    path('formatter_result',views.formatter_result, name = 'formatter_result'),
    path('download_csv_array',views.download_csv_array, name = 'download_csv_array'),
    path('download_csv_column',views.download_csv_column, name = 'download_csv_column'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)