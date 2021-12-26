from django.conf import settings
from django.db import models
from django.utils import timezone
import datetime
import os

media_root = settings.MEDIA_ROOT

empty_path = os.path.join(media_root, 'empty.csv')
class Csv(models.Model):
    csv_file = models.FileField(upload_to='media')
    csv_file_control = models.FileField(upload_to='media', default=empty_path)

