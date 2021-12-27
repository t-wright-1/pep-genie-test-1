import os
from django.conf import settings
from django.shortcuts import render
from lab.seq_studies import *
from lab.formatter import *
from django.http import HttpResponse, Http404

from .models import Csv
from .forms import CsvForm

media_root = settings.MEDIA_ROOT



# Create your views here.
def resources(request):
    return render(request, 'lab/resources.html')

def sequence_studies(request):
    return render(request, 'lab/sequence_studies.html')

def ss_result(request):
    res=''
    seq = request.POST.get('enter-sequence').upper()
    m_notation_box = request.POST.get('m-notation')

    ala_box = request.POST.get('ala-scan')
    if ala_box == 'true':
        res += ala_scan(seq)
        res += '\n'
        if m_notation_box == 'true':
            res += '.space'
            res += '\n'
            res += '\n'

    n_trunc_box = request.POST.get('n-trunc')
    if n_trunc_box == 'true':
        res += n_trunc(seq)
        res += '\n'
        if m_notation_box == 'true':
            res += '.space'
            res += '\n'
            res += '\n'

    c_trunc_box = request.POST.get('c-trunc')
    if c_trunc_box == 'true':
        res += c_trunc(seq)
        res += '\n'
        if m_notation_box == 'true':
            res += '.space'
            res += '\n'
            res += '\n'

    n_c_trunc_box = request.POST.get('n-c-trunc')
    if n_c_trunc_box == 'true':
        res += n_c_trunc(seq)
        res += '\n'
        if m_notation_box == 'true':
            res += '.space'
            res += '\n'
            res += '\n'

    point_sub_box = request.POST.get('point-sub')
    if point_sub_box == 'true':
        res += point_sub(seq)
        res += '\n'
        if m_notation_box == 'true':
            res += '.space'
            res += '\n'
            res += '\n'
    return render(request, "lab/ss_result.html", {"result":res})

def formatter(request):
    form = CsvForm()
    return render(request, 'lab/2-1_formatter.html',{'form':form})

def formatter_result(request):
    #Validate form and save model
    if request.method == 'POST':
        form = CsvForm(request.POST, request.FILES)
        if form.is_valid():
            print('VALID')
            form.save()

            #Load model to python and set file paths
            my_model = Csv.objects.all().order_by('-id')[0]
            array_path = os.path.join(media_root, my_model.csv_file.name)
            array_control_path = os.path.join(media_root, my_model.csv_file_control.name)

            #Check for normalisation
            if my_model.csv_file_control == os.path.join(media_root, my_model.csv_file_control.name):
                normalisation = 'False'
            else:
                normalisation = 'True'

            #process csvs and make heatmap
            Formatter(array_path, array_control_path, normalisation)

            #pass heatmap to context
            heatmap_path = os.path.join('media', 'heatmap.png')

            #debugging
            print(os.path.join('media', 'csv_array.csv'))
            print('Abs path')
            print('/Users/Tom/Python_Projects/project_13/media/csv_array.csv')
            print('rel path')
            print('media/csv_array.csv')
            print('suggested fix')
            print(os.path.join(media_root,'csv_array.csv'))


            return render(request, 'lab/2-2_formatter_result.html', {'heatmap_path':heatmap_path}) 
        else:
            print('NO, form is not valid')
    return render(request, "lab/2-2_formatter_result.html")

def download_csv_array(request):
    #Original error source: file_path=os.path.join('media','csv_array.csv')
    file_path=os.path.join(media_root,'csv_array.csv')

    if os.path.exists(file_path): #!!!!!!!!!!!!!!!!!
        print('Path Exists')
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/default")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    print('Path does not exist')
    raise Http404

def download_csv_column(request):
    #file_path=os.path.join('media','csv_column.csv')
    file_path=os.path.join(media_root,'csv_column.csv')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/default")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
    




