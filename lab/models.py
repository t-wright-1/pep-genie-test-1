from email.policy import default
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import validate_image_file_extension

import datetime
import os
import random

media_root = settings.MEDIA_ROOT
lab_root = settings.LAB_ROOT
lab_static = settings.LAB_STATIC
seven_root = os.path.join(media_root,'7')

empty_path = os.path.join(media_root, 'empty.csv')
dummy_url = os.path.join(lab_root, 'dummy.png')
example_array ='/images/example-array.jpg'
example_array2 = '/images/example-array_2.jpg'
vis_array = '/images/vis_blank_iNC1Mxm.jpg'

static_folder = settings.STATIC_FOLDER
member_blank_url = os.path.join(static_folder, 'member-blank.jpg')


def two_dir(instance, filename):
    return '{0}/{1}/{2}'.format('2',instance.user_id,filename)
class Csv(models.Model):
    user_id = models.CharField(max_length=100)
    csv_file = models.FileField(upload_to=two_dir)
    csv_file_control = models.FileField(upload_to=two_dir, default=empty_path)




def three_dir(instance, filename):
    return '{0}/{1}/{2}'.format('3',instance.user_id,filename)
class WheelModel(models.Model):
    user_id = models.CharField(max_length=100)
    sequence = models.CharField(max_length=100)
    first_res = models.IntegerField(default=1)
    surface_mode = models.BooleanField(null=True, blank=False)
    surface_data = models.CharField(max_length=100, null=True, blank=True)
    colour_scheme = models.CharField(max_length=100)
    wheel = models.FileField(upload_to=three_dir, default=empty_path)




def four_dir(instance, filename):
    return '{0}/{1}/{2}'.format('4',instance.user_id,filename)
class CropModel(models.Model):
    user_id = models.CharField(max_length=100)
    crop_image = models.FileField(upload_to=four_dir)
    rows = models.IntegerField(default=20)
    cols = models.IntegerField(default=4)
    full_grid = models.ImageField(upload_to=four_dir,default=dummy_url)
    coords = models.CharField(max_length=200, default = 'empty')
    cropped_image = models.ImageField(upload_to=four_dir,default=dummy_url, null=True)




def five_dir(instance, filename):
    return '{0}/{1}/{2}'.format('5',instance.user_id,filename)
class AutoCropModel(models.Model):
    user_id = models.CharField(max_length=100)
    vis = models.FileField(upload_to=five_dir)
    vis_trn = models.FileField(upload_to=five_dir)
    crop_image = models.FileField(upload_to=five_dir)
    rows = models.IntegerField(default=20)
    cols = models.IntegerField(default=4)
    full_grid = models.ImageField(upload_to=five_dir,default=dummy_url)
    trn_coords = models.CharField(max_length=200, default = 'empty')
    crop_coords = models.CharField(max_length=200, default = 'empty')
    cropped_image = models.ImageField(upload_to=five_dir,default=dummy_url, null=True)




def six_dir(instance, filename):
    return '{0}/{1}/{2}'.format('6',instance.user_id,filename)
class StripModel(models.Model):
    user_id = models.CharField(max_length=100)
    rows = models.IntegerField(default=20)
    cols = models.IntegerField(default=4)
    first_col = models.IntegerField(default=8)
    test_image = models.FileField(upload_to=six_dir)
    mock_image = models.ImageField(upload_to=six_dir,default=dummy_url, null=True)
    strip_request = models.CharField(max_length=100, default='A08-T08,A09-T09')




def new_dir(instance, filename):
    return '{0}/{1}/{2}'.format('7',instance.user_id,filename)
    #challenge was saving files to new directory by referencing self field value
    #Watch the commas here for the url in the template. Need no comma here
class SevenModel(models.Model):
    user_id = models.CharField(max_length=100)

    strip_request = models.CharField(max_length=100, default='A08-T08,A09-T09')
    rows = models.IntegerField(default=20)
    cols = models.IntegerField(default=4)
    first_col = models.IntegerField(default=8)

    full_grid = models.ImageField(upload_to=new_dir,default=dummy_url)

    auto = models.BooleanField(null=True, blank=True)

    test_image = models.FileField(upload_to=new_dir)
    test_coords = models.CharField(max_length=200, default = 'empty')

    mock_image = models.FileField(upload_to=new_dir)
    mock_coords = models.CharField(max_length=200, default = 'empty')

    vis = models.FileField(upload_to=new_dir, default=empty_path)
    vis_trn = models.FileField(upload_to=new_dir)
    trn_coords = models.CharField(max_length=200, default = 'empty')


my_url = os.path.join('static','lab')
class MemberModel(models.Model):
    PI = "PI"
    POST_DOC = "POST_DOC"
    POST_GRAD = "POST_GRAD"
    MASTER = "MASTER"
    LAB_MANAGER = "LAB_MANAGER"
    LAB_TECH = "TECHNICIAN"
    TITLE_CHOICES = [
        (PI, "Principal Investigator"),
        (POST_DOC, "Postdoctoral Researcher"),
        (POST_GRAD, "Postgraduate Student"),
        (MASTER, "Masters Student"),
        (LAB_MANAGER, "Lab Manager"),
        (LAB_TECH, "Technician")
    ]
    name = models.CharField(max_length=100)
    year = models.IntegerField(default=2000)
    profile = models.FileField(upload_to=my_url, default=member_blank_url)
    title = models.CharField(max_length=100,choices=TITLE_CHOICES, default=POST_GRAD)
    bio = models.TextField()
    handles = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def clean(self):
        if self.title == "LAB_MANAGER":
            model = self.__class__
            my_list = model.objects.filter(title='LAB_MANAGER')
            if len(my_list) >= 1:
                raise ValidationError("You can only set one lab manager. Please delete the current lab manager instance before creating a new one.")
        if self.title == "PI":
            model = self.__class__
            my_list = model.objects.filter(title='PI')
            if len(my_list) >= 1:
                raise ValidationError("You can only set one Principle Investigator. Please delete the current instance before creating a new one.")
    
def news_post_dir(instance, filename):
    return '{0}/{1}'.format('news_images',filename)
class PostModel(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    picture = models.FileField(upload_to=news_post_dir)
    text = models.TextField()

    def __str__(self):
        return self.title




def signal_dir(instance, filename):
    return '{0}/{1}'.format('signal',filename)
class SignalModel(models.Model):
    rows = models.IntegerField(default=20)
    cols = models.IntegerField(default=4)
    first_col = models.IntegerField(default=8)
    full_grid = models.ImageField(upload_to=signal_dir,default=dummy_url)
    crop_coords = models.CharField(max_length=200, default = 'empty')
    img = models.FileField(upload_to=signal_dir)
    img_crop = models.ImageField(upload_to=signal_dir,default=dummy_url, null=True)
    strip_request = models.CharField(max_length=1000, default='A08-T08,A09-T09')
    graph_types = models.CharField(max_length=1000, default='null')
    dens_list = models.CharField(max_length=1000, default='null')
    csv = models.FileField(upload_to=signal_dir)





def sd_dir(instance, filename):
    return '{0}/{1}/{2}'.format('sd',instance.user_id,filename)

class SDModel(models.Model):

    #form 
    cols = models.IntegerField(default=4)
    first_col = models.IntegerField(default=8)
    strip_request = models.CharField(max_length=1000, default='A08-T08,A09-T09')
    graph_types = models.CharField(max_length=1000, default='v')
    norm = models.BooleanField(default=False)

    img_1 = models.FileField(upload_to=sd_dir, validators=[validate_image_file_extension])
    img_1_crop = models.ImageField(upload_to=sd_dir,default=dummy_url, null=True)
    img_1_coords = models.CharField(max_length=200, default = 'empty')
    img_1_csv = models.FileField(upload_to=sd_dir)

    img_2 = models.FileField(upload_to=sd_dir)
    img_2_crop = models.ImageField(upload_to=sd_dir,default=dummy_url, null=True)
    img_2_coords = models.CharField(max_length=200, default = 'empty')
    img_2_csv = models.FileField(upload_to=sd_dir)

    #gen
    user_id = models.CharField(max_length=100)
    ppt_path = models.CharField(max_length=100)
    full_grid = models.ImageField(upload_to=sd_dir,default=dummy_url)
    dens_list = models.CharField(max_length=1000, default='null')
    config = models.CharField(max_length=1000, default="{'c':0}") #user_id,  
    normalised_csv = models.FileField(upload_to=sd_dir)   


