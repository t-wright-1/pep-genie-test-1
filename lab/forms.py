from django import forms 
from .models import Csv, SignalModel
from .models import CropModel
from .models import AutoCropModel
from .models import StripModel
from .models import SevenModel
from .models import WheelModel

class CsvForm(forms.ModelForm):
    class Meta:
        model = Csv
        fields = ('csv_file','csv_file_control')
        labels = {
        "csv_file": "Csv File:",
        "csv_file_control": "Control Csv File:"
        }


class WheelModelForm(forms.ModelForm):
    BLUE = 0
    GREY = 1
    RED_BLUE = 2
    VIRIDIS = 3
    BONE = 4
    CHOICES = (
        (BLUE,'Blue'),
        (GREY,'Grey'),
        (RED_BLUE,'Red-Blue'),
        (VIRIDIS,'Viridis'),
        (BONE,'Bone'),
    )
    
    colour_scheme = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = WheelModel
        fields = ('sequence','first_res','surface_data','colour_scheme')
        labels = {
        "sequence": "Helix Sequence:",
        "first_res": "Number of First Residue:",
        "surface_data": "Please enter your surface data:",
        "colour_scheme":"Colour Scheme:"
        }




class CropModelForm(forms.ModelForm):
    class Meta:
        model = CropModel
        fields = ('crop_image','rows','cols')
        labels = {
        "crop_image": "Image to Crop:",
        "rows": "Rows:",
        "cols": "Columns:",
        }

class AutoCropModelForm(forms.ModelForm):
    class Meta:
        model = AutoCropModel
        fields = ('vis','crop_image','rows','cols')
        labels = {
        "crop_image": "Image to Crop:",
        "vis":"Photo of Array:",
        "rows": "Rows:",
        "cols": "Columns:",
        }

class StripModelForm(forms.ModelForm):
    class Meta:
        model = StripModel
        fields = ('test_image','mock_image','rows','cols','first_col','strip_request')
        labels = {
        "test_image": "Test Image:",
        "mock_image":"Mock Image:",
        "rows": "Rows:",
        "cols": "Columns:",
        "first_col": "Number of First Column:",
        "strip_request": "Please Enter your Strips:",
        }

class SevenModelForm(forms.ModelForm):
    class Meta:
        model = SevenModel
        fields = ('test_image','mock_image','vis','rows','cols','first_col','strip_request')
        labels = {
        "test_image": "1) Test Image:",
        "mock_image":"2) Mock Image:",
        "vis":"Photo of Array:",
        "rows": "4) Rows:",
        "cols": "5) Columns:",
        "first_col": "6) Number of First Column:",
        "strip_request": "7) Please Enter your Strips:",
        }



class SignalModelForm(forms.ModelForm):
    class Meta:
        model = SignalModel
        fields = ('img','cols','rows','first_col')
        labels = {
        "img": "Array Image",
        "cols": "Number of Columns",
        "rows": "Number of Rows",
        "first_col": "Number of First Column",
        }
