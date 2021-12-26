from django import forms 
from .models import Csv

class CsvForm(forms.ModelForm):
    class Meta:
        model = Csv
        fields = ('csv_file','csv_file_control')
        labels = {
        "csv_file": "Csv File:",
        "csv_file_control": "Control Csv File:"
        }
