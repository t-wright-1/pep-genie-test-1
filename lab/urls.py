from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'lab'

urlpatterns = [
    path('',views.index, name = 'index'),
    path('resources',views.resources, name = 'resources'),
    path('resources_2',views.resources_2, name = 'resources_2'),
    path('team',views.team, name = 'team'),
    path('member',views.member, name = 'member'),
    path('george',views.george, name = 'george'),
    path('news',views.news, name = 'news'),

    path('sequence_studies',views.sequence_studies, name = 'sequence_studies'),
    
    path('ss_result',views.ss_result, name = 'ss_result'),
    path('formatter',views.formatter, name = 'formatter'),
    path('formatter_result',views.formatter_result, name = 'formatter_result'),
    path('download_csv_array',views.download_csv_array, name = 'download_csv_array'),
    path('download_csv_column',views.download_csv_column, name = 'download_csv_column'),

    path('wheel_upload',views.wheel_upload, name = 'wheel_upload'),
    path('wheel_result',views.wheel_result, name = 'wheel_result'),
    path('wheel_download',views.wheel_download, name = 'wheel_download'),

    path('crop_upload',views.crop_upload, name = 'crop_upload'),
    path('crop_grid',views.crop_grid, name = 'crop_grid'),
    path('crop_result',views.crop_result, name = 'crop_result'),
    path('crop_download',views.crop_download, name = 'crop_download'),

    path('auto_crop_upload',views.auto_crop_upload, name = 'auto_crop_upload'),
    path('auto_crop_trn',views.auto_crop_trn, name = 'auto_crop_trn'),
    path('auto_crop_grid',views.auto_crop_grid, name = 'auto_crop_grid'),
    path('auto_crop_adjust',views.auto_crop_adjust, name = 'auto_crop_adjust'),
    path('auto_crop_result',views.auto_crop_result, name = 'auto_crop_result'),
    path('auto_crop_download',views.auto_crop_download, name = 'auto_crop_download'),

    path('strip_upload',views.strip_upload, name = 'strip_upload'),
    path('strip_result',views.strip_result, name = 'strip_result'),
    path('strip_download',views.strip_download, name = 'strip_download'),

    path('strip_1',views.strip_1, name = 'strip_1'),
    path('strip_2a',views.strip_2a, name = 'strip_2a'),
    path('strip_2b_1',views.strip_2b_1, name = 'strip_2b_1'),
    path('strip_2b_2',views.strip_2b_2, name = 'strip_2b_2'),
    path('strip_2b_3',views.strip_2b_3, name = 'strip_2b_3'),
    path('strip_3',views.strip_3, name = 'strip_3'),
    path('strip_4',views.strip_4, name = 'strip_4'),
    path('strip_5',views.strip_5, name = 'strip_5'),

    path('signal',views.signal, name = 'signal'),
    path('signal_2',views.signal_2, name = 'signal_2'),
    path('signal_3',views.signal_3, name = 'signal_3'),
    path('signal_4',views.signal_4, name = 'signal_4'),
 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)