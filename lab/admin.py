from django.contrib import admin
from .models import AutoCropModel, Csv
from .models import CropModel
from .models import AutoCropModel
from .models import StripModel
from .models import SevenModel
from .models import WheelModel
from .models import MemberModel, PostModel


# Register your models here.

admin.site.register(Csv)
admin.site.register(CropModel)
admin.site.register(AutoCropModel)
admin.site.register(StripModel)
admin.site.register(SevenModel)
admin.site.register(WheelModel)
admin.site.register(MemberModel)
admin.site.register(PostModel)