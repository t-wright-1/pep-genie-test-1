from genericpath import exists
import os
from django.conf import settings
from django.shortcuts import render, redirect
from lab.seq_studies import *
from lab.formatter import *
from lab.grid_generator import *
from lab.pytools import *
from lab.wheel_generator import generate_wheel
from django.http import HttpResponse, Http404, HttpResponseServerError
max_ = max;
min_ = min;
from cv2 import *
from django.core.files.base import ContentFile
from PIL import Image
from lab.strip_ppt import *
from datetime import datetime
import numpy
import ast
import random

from .models import Csv, MemberModel, SignalModel, SDModel
from .models import CropModel
from .models import AutoCropModel
from .models import StripModel
from .models import SevenModel
from .models import WheelModel
from .models import PostModel

from .forms import CsvForm, SignalModelForm, SignalModelForm2, SDModelForm
from .forms import CropModelForm
from .forms import AutoCropModelForm
from .forms import StripModelForm
from .forms import SevenModelForm
from .forms import WheelModelForm

media_root = settings.MEDIA_ROOT
lab_root = settings.LAB_ROOT
lab_static_root = settings.LAB_STATIC_ROOT
base_dir = settings.BASE_DIR
strips_root = settings.STRIPS_ROOT

two_root = os.path.join(media_root,'2')
three_root = os.path.join(media_root,'3')
four_root = os.path.join(media_root,'4')
five_root = os.path.join(media_root,'5')
six_root = os.path.join(media_root,'6')
seven_root = os.path.join(media_root,'7')

# Create your views here.









def index(request):
    return render(request, 'lab/index.html')

def team(request):
    for member in MemberModel.objects.all():
        print(member.title)
    PI = MemberModel.objects.filter(title='PI')
    post_docs = MemberModel.objects.filter(title='POST_DOC')
    phds = MemberModel.objects.filter(title='POST_GRAD')
    masters = MemberModel.objects.filter(title='MASTER')
    lab_manager = MemberModel.objects.filter(title='LAB_MANAGER')[0]
    lab_techs = MemberModel.objects.filter(title='TECHNICIAN')

    post_doc_filled=True
    if not post_docs:
        post_doc_filled = False

    phds_filled=True
    if not phds:
        phds_filled = False

    masters_filled=True
    if not masters:
        masters_filled = False

    lab_techs_filled=True
    if not lab_techs:
        lab_techs_filled=False


    context = {
        'PI':PI,
        'post_docs':post_docs,
        'phds':phds,
        'masters':masters,
        'lab_manager':lab_manager,
        'lab_techs':lab_techs,

        'post_doc_filled':post_doc_filled,
        'phds_filled':phds_filled,
        'masters_filled':masters_filled,
        'lab_techs_filled':lab_techs_filled,
    }
    return render(request, 'lab/team2.html',context)

def member(request):
    member_name = request.POST.get('team-input')
    my_model = MemberModel.objects.filter(name=member_name)[0]
    title = ''
    if my_model.title == 'PI':
        title = 'Principle Investigator'
    elif my_model.title == 'POST_DOC':
        title = 'Postdoctoral Researcher'
    elif my_model.title == 'POST_GRAD':
        title = 'Postgraduate Researcher'
    elif my_model.title == 'MASTER':
        title = 'Masters Student'
    elif my_model.title == 'LAB_MANAGER':
        title = 'Lab Manager'
    elif my_model.title == 'LAB_TECH':
        title = 'Lab Technician'

    handle_list = []
    temp_list = []
    for i in my_model.handles:
        if i != ' ':
            temp_list.append(i)
    temp_str = ''.join(map(str, temp_list))
    handle_list = temp_str.split(',')
    context = {
        'my_model':my_model,
        'title':title,
        'handle_list':handle_list
    }
    return render(request, 'lab/member.html',context)

def george(request):
    member_name = "George Baillie"
    my_model = MemberModel.objects.filter(name=member_name)[0]

    handle_list = []
    temp_list = []
    for i in my_model.handles:
        if i != ' ':
            temp_list.append(i)
    temp_str = ''.join(map(str, temp_list))
    handle_list = temp_str.split(',')
    context = {
        'my_model':my_model,
        'handle_list':handle_list
    }
    return render(request, 'lab/george.html',context)

def resources(request):
    return render(request, 'lab/resources.html')

def resources_2(request):
    return render(request, 'lab/resources_2.html')

def news(request):
    my_models = PostModel.objects.all()
    context = {'my_models':my_models}
    return render(request, 'lab/news.html', context)

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
    #remove previous csv models and files
    '''for model in Csv.objects.all():

        old_file_path = os.path.join(media_root,model.csv_file.name)
        if os.path.exists(old_file_path):
            os.remove(old_file_path)

        if model.csv_file_control.name != '/Users/Tom/Python_Projects/project_13/media/empty.csv':
            old_file_path_control = os.path.join(media_root,model.csv_file_control.name)
            if os.path.exists(old_file_path_control):
                os.remove(old_file_path_control)

    Csv.objects.all().delete()'''

    #make new instance and set user_id as four digit number
    hash = random.randint(1111,9999)
    my_model = Csv(user_id=hash)
    my_model.save()
    #load form of that existing instance
    form = CsvForm(instance = my_model)
    return render(request, 'lab/2-1_formatter.html', {'form':form})

def formatter_result(request):
    #Validate form and save model
    my_model = Csv.objects.all().order_by('-id')[0]
    if request.method == 'POST':
        form = CsvForm(request.POST, request.FILES,instance=my_model)
        if form.is_valid():
            form.save()
            #Load model to python and set file paths
            array_path = os.path.join(media_root, my_model.csv_file.name)
            array_control_path = os.path.join(media_root, my_model.csv_file_control.name)

            #Check for normalisation
            if my_model.csv_file_control == os.path.join(media_root, my_model.csv_file_control.name):
                normalisation = 'False'
            else:
                normalisation = 'True'

            #process csvs and make heatmap
            id_root = os.path.join(two_root, my_model.user_id)
            Formatter(array_path, array_control_path, normalisation, id_root)

            #pass heatmap to context
            path_0 = os.path.join('media','2')
            path_1 = os.path.join(path_0,my_model.user_id)
            path_2 = os.path.join(path_1,'heatmap.png')
            heatmap_path = path_2

            return render(request, 'lab/2-2_formatter_result.html', {'heatmap_path':heatmap_path}) 
        else:
            print('NO, form is not valid')
    return render(request, "lab/2-2_formatter_result.html")

def download_csv_array(request):
    #Original error source: file_path=os.path.join('media','csv_array.csv')
    file_path=os.path.join(media_root,'csv_array.csv')

    if os.path.exists(file_path): #!!!!!!!!!!!!!!!!!

        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/default")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

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
    








def wheel_upload(request):
    #make new instance and set user_id as four digit number
    hash = random.randint(1111,9999)
    my_model = WheelModel(user_id=hash)
    my_model.save()
    my_path = os.path.join(three_root, str(hash))
    os.mkdir(my_path)
    #load form of that existing instance
    form = WheelModelForm(instance = my_model)
    return render(request, 'lab/3-1_upload.html', {'form':form})

def wheel_result(request):
    #Validate form and save model
    my_model = WheelModel.objects.all().order_by('-id')[0]
    if request.method == 'POST':
        form = WheelModelForm(request.POST, request.FILES, instance=my_model)
        form.save()
        if form.is_valid():
            form.save()
    else:
        print('NOT VALID')
        return HttpResponseServerError()
    #save surface_mode to model
    my_model.surface_mode = request.POST.get('surface_box')
    my_model.colour_scheme = request.POST.get('colour_scheme')
    my_model.save()
    print('SURFACE_MODE AT MODE',my_model.surface_mode)
    print(request.POST)
    #get variables    
    id_root = os.path.join(three_root,my_model.user_id)
    file_name = 'wheel_' + my_model.user_id + '.png'
    my_path = os.path.join(id_root, file_name)
    if my_model.surface_data == None:
        surface_data = None
    else:
        surface_data = ast.literal_eval(my_model.surface_data)
    #generate_wheel(my_model.sequence, my_path, my_model.first_res, my_model.surface_mode, ast.literal_eval(my_model.surface_data))
    generate_wheel(my_model.sequence, my_path, my_model.first_res, my_model.surface_mode, surface_data, my_model.colour_scheme)
    
    my_plot = cv2.imread(my_path)
    
    #save wheel to model
    ret, buf = cv2.imencode('.png', my_plot) 
    content = ContentFile(buf.tobytes())
    my_model.wheel.save(file_name, content)
    my_model.save() 

    return render(request, 'lab/3-2_result.html', {'my_model':my_model})

def wheel_download(request):
    #Original error source: file_path=os.path.join('media','csv_array.csv')
    my_model = WheelModel.objects.all().order_by('-id')[0]
    id_root = os.path.join(three_root,my_model.user_id)
    file_name = 'wheel_' + my_model.user_id + '.png'
    my_path = os.path.join(id_root, file_name)
    if os.path.exists(my_path): 
        with open(my_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/default")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(my_path)
            return response

    raise Http404










def crop_upload(request):
    #make new instance and set user_id as four digit number
    hash = random.randint(1111,9999)
    my_model = CropModel(user_id=hash)
    my_model.save()
    #load form of that existing instance
    form = CropModelForm(instance = my_model)
    return render(request, 'lab/4-1_upload.html', {'form':form})

def crop_grid(request):
    #Validate form and save model
    my_model = CropModel.objects.all().order_by('-id')[0]
    if request.method == 'POST':
        form = CropModelForm(request.POST, request.FILES, instance=my_model)
        form.save()
        if form.is_valid():
            form.save()
    else:
        print('NOT VALID')

    #generate grid file
    rows = my_model.rows
    cols = my_model.cols
    grid_unit_path = os.path.join(lab_static_root, 'grid-unit.png')
    full_grid = generate_grid(rows,cols,grid_unit_path)

    #save full grid to model
    ret, buf = cv2.imencode('.png', full_grid) 
    content = ContentFile(buf.tobytes())
    my_model.full_grid.save('full_grid.png', content)
    my_model.save()    
    context = {
        'my_model':my_model,
    }
    return render(request, "lab/4-2_grid.html", context)

def crop_result(request):
    x1 = float(request.POST.get('coordX1'))
    y1 = float(request.POST.get('coordY1'))
    x2 = float(request.POST.get('coordX2'))
    y2 = float(request.POST.get('coordY2'))
    my_coords = [x1,y1,x2,y2]

    my_model = CropModel.objects.all().order_by('-id')[0]
    my_model.coords = my_coords
    my_model.save()

    test_coords = my_coords
    test_x1 = test_coords[0]
    test_y1 = test_coords[1]
    test_x2 = test_coords[2]
    test_y2 = test_coords[3]

    #crop image
    my_url = os.path.join(media_root,my_model.crop_image.name)
    image = Image.open(my_url)

    width, height = image.size

    left = float(test_x1)*float(width)
    upper = float(test_y1)*float(height)
    right = float(test_x2)*float(width)
    lower = float(test_y2)*float(height)

    overlay_image_cropped = image.crop((left, upper, right, lower))

    #convert PIL to openCV
    open_cv_image = numpy.array(overlay_image_cropped) 
    # Convert RGB to BGR 
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

    #save cropped_image to model
    ret, buf = cv2.imencode('.png', open_cv_image) 
    content = ContentFile(buf.tobytes())
    my_model.cropped_image.save('cropped.png', content)
    my_model.save()    
    
    return render(request, 'lab/4-3_result.html', {'my_model':my_model})

def crop_download(request):
    #Original error source: file_path=os.path.join('media','csv_array.csv')
    my_model = CropModel.objects.all().order_by('-id')[0]
    file_path = os.path.normpath(str(base_dir)+my_model.cropped_image.url)
    print(file_path)
    if os.path.exists(file_path): #!!!!!!!!!!!!!!!!!

        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/default")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

    raise Http404







def auto_crop_upload(request):
    #make new instance and set user_id as four digit number
    hash = random.randint(1111,9999)
    my_model = AutoCropModel(user_id=hash)
    my_model.save()
    #load form of that existing instance
    form = AutoCropModelForm(instance = my_model)
    return render(request, 'lab/5-1_upload.html', {'form':form})

def auto_crop_trn(request):
    #Validate form and save model
    my_model = AutoCropModel.objects.all().order_by('-id')[0]
    if request.method == 'POST':
        form = AutoCropModelForm(request.POST, request.FILES, instance=my_model)
        form.save()
        if form.is_valid():
            form.save()
    else:
        print('NOT VALID')
        return HttpResponseServerError()
    my_model = AutoCropModel.objects.all().order_by('-id')[0]
    context = {
        "my_model":my_model
    }
    return render(request, 'lab/5-2_trn.html',context)


def auto_crop_grid(request):
    trn_coords = request.POST.get('vis-coords')
    my_model = AutoCropModel.objects.all().order_by('-id')[0]
    my_model.trn_coords = trn_coords
    vis_url = os.path.join(media_root,my_model.vis.name)
    trans_img = four_point_transform(vis_url, trn_coords)
    #save transformed image to model
    ret, buf = cv2.imencode('.jpg', trans_img) # cropped_image: cv2 / np array
    content = ContentFile(buf.tobytes())
    my_model.vis_trn.save('image.jpg', content)
    my_model.save()
    #generate grid file
    rows = my_model.rows
    cols = my_model.cols
    grid_unit_path = os.path.join(lab_static_root, 'grid-unit.png')
    full_grid = generate_grid(rows,cols,grid_unit_path)
    #save full grid to model
    ret, buf = cv2.imencode('.png', full_grid) 
    content = ContentFile(buf.tobytes())
    my_model.full_grid.save('full_grid.png', content)
    my_model.save()    
    #context
    full_grid_url = os.path.join(media_root,my_model.full_grid.name)
    context = {
        'my_model':my_model,
        'full_grid_url':full_grid_url,
        'grid_name':my_model.full_grid.name,
    }
    return render(request, 'lab/5-3_grid.html', context)

def auto_crop_adjust(request):
    x1 = float(request.POST.get('coordX1'))
    y1 = float(request.POST.get('coordY1'))
    x2 = float(request.POST.get('coordX2'))
    y2 = float(request.POST.get('coordY2'))
    canvas_width = float(request.POST.get('canvas_width'))
    canvas_height = float(request.POST.get('canvas_height'))
    my_coords = [x1,y1,x2,y2]
    my_model = AutoCropModel.objects.all().order_by('-id')[0]
    #my_model.crop_coords = my_coords
    #my_model.save()
    #context
    top = str(y1 * canvas_height) + 'px'
    height = str((y2-y1) * canvas_height) + 'px'
    left = str(x1 * canvas_width) + 'px'
    width = str((x2-x1) * canvas_width) + 'px'
    full_grid_url = os.path.join(media_root,my_model.full_grid.name)
    context = {
        'my_model':my_model,
        'full_grid_url':full_grid_url,
        'grid_name':my_model.full_grid.name,
        'top':top,
        'left':left,
        'width':width,
        'height':height,
        'se_left': str( (x1 * canvas_width) + ((x2-x1) * canvas_width) ) + 'px',
        'se_top': str(y1 * canvas_height)  + 'px',
    }
    return render(request, 'lab/5-4_adjust.html', context)

def auto_crop_result(request):
    x1 = float(request.POST.get('coordX1'))
    y1 = float(request.POST.get('coordY1'))
    x2 = float(request.POST.get('coordX2'))
    y2 = float(request.POST.get('coordY2'))
    my_coords = [x1,y1,x2,y2]

    my_model = AutoCropModel.objects.all().order_by('-id')[0]
    my_model.coords = my_coords
    my_model.save()

    test_coords = my_coords
    test_x1 = test_coords[0]
    test_y1 = test_coords[1]
    test_x2 = test_coords[2]
    test_y2 = test_coords[3]

    #crop image
    my_url = os.path.join(media_root,my_model.crop_image.name)
    image = Image.open(my_url)
    width, height = image.size

    left = float(test_x1)*float(width)
    upper = float(test_y1)*float(height)
    right = float(test_x2)*float(width)
    lower = float(test_y2)*float(height)

    overlay_image_cropped = image.crop((left, upper, right, lower))

    #convert PIL to openCV
    open_cv_image = numpy.array(overlay_image_cropped) 
    # Convert RGB to BGR 
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

    #save cropped_image to model
    ret, buf = cv2.imencode('.png', open_cv_image) 
    content = ContentFile(buf.tobytes())
    my_model.cropped_image.save('cropped.png', content)
    my_model.save()    
    
    return render(request, 'lab/5-5_result.html', {'my_model':my_model})

def auto_crop_download(request):
    #Original error source: file_path=os.path.join('media','csv_array.csv')
    my_model = AutoCropModel.objects.all().order_by('-id')[0]
    file_path = os.path.normpath(str(base_dir)+my_model.cropped_image.url)
    print(file_path)
    if os.path.exists(file_path): #!!!!!!!!!!!!!!!!!

        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/default")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

    raise Http404









def strip_upload(request):
    #make new instance and set user_id as four digit number
    hash = random.randint(1111,9999)
    my_model = StripModel(user_id=hash)
    my_model.save()
    #load form of that existing instance
    form = StripModelForm(instance = my_model)
    return render(request, 'lab/6-1_upload.html', {'form':form})

def strip_result(request):
    #Validate form and save model
    my_model = StripModel.objects.all().order_by('-id')[0]
    if request.method == 'POST':
        form = StripModelForm(request.POST, request.FILES, instance=my_model)
        form.save()
        if form.is_valid():
            form.save()
    else:
        print('NOT VALID')
        return HttpResponseServerError()
    #get variables    
    my_model = StripModel.objects.all().order_by('-id')[0]
    #print(strip_number(my_model.strip_request,my_model.first_col)) = [[1, 20], [21, 40]]
    strip_request = strip_number(my_model.strip_request,my_model.first_col)
    test_image_path = os.path.join(media_root,my_model.test_image.name)
    test_strips = stripper(test_image_path,my_model.rows,my_model.cols,strip_request)
    mock_image_path = os.path.join(media_root,my_model.mock_image.name)
    mock_strips = stripper(mock_image_path,my_model.rows,my_model.cols,strip_request)
    
    #save strips to folder for pptx
    id_root = os.path.join(six_root,my_model.user_id)
    for i in range(len(test_strips)):
        my_filename = 'strip_' + str(i)+'.png'
        test_strips[i].save(os.path.join(id_root,my_filename)) 

    for i in range(len(mock_strips)):
        my_filename = 'mock_strip_' + str(i)+'.png'
        mock_strips[i].save(os.path.join(id_root,my_filename)) 

    make_pptx(test_strips,strip_request,id_root,my_model.user_id)

    return render(request, 'lab/6-2_result.html')

def strip_download(request):
    #Original error source: file_path=os.path.join('media','csv_array.csv')
    my_model = StripModel.objects.all().order_by('-id')[0]
    pres_name = 'presentation_'+my_model.user_id+'.pptx'

    id_root = os.path.join(six_root, my_model.user_id)
    file_path = os.path.join(id_root, pres_name)

    if os.path.exists(file_path): 
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/default")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

    raise Http404








def strip_1(request):
    #make new instance and set user_id as four digit number
    hash = random.randint(1111,9999)
    my_model = SevenModel(user_id=hash)
    my_model.save()
    #load form of that existing instance
    form = SevenModelForm(instance = my_model)
    return render(request, 'lab/7-1_upload.html', {'form':form})

def strip_2a(request):
    #Validate form and save model
    my_model = SevenModel.objects.all().order_by('-id')[0]
    if request.method == 'POST':
        form = SevenModelForm(request.POST, request.FILES, instance = my_model)
        form.save()
        if form.is_valid():
            form.save()
    else:
        print('NOT VALID')
        return HttpResponseServerError()
    #Set auto
    my_model = SevenModel.objects.all().order_by('-id')[0]
    my_auto = request.POST.get('auto_mock_box',0)
    my_model.auto = my_auto
    my_model.save()
    #generate grid file
    rows = my_model.rows
    cols = my_model.cols
    grid_unit_path = os.path.join(lab_static_root, 'grid-unit.png')
    full_grid = generate_grid(rows,cols,grid_unit_path)
    #save full grid to model
    ret, buf = cv2.imencode('.png', full_grid) 
    content = ContentFile(buf.tobytes())
    my_model.full_grid.save('full_grid.png', content)
    my_model.save() 
    #redirect if auto == True
    if my_auto == 'True':
        return redirect('lab:strip_2b_1') 
    #render 
    full_grid_url = os.path.join(media_root,my_model.full_grid.name)
    print(my_model, full_grid_url, my_model.full_grid.name)
    context = {
        'my_model':my_model,
    }
    return render(request, "lab/7-2a_mock.html", context)

def strip_2b_1(request):
    my_model = SevenModel.objects.all().order_by('-id')[0]
    return render(request, 'lab/7-2b-1_vis_trn.html',{'my_model':my_model})

def strip_2b_2(request):
    #get trn coords and transform image
    trn_coords = request.POST.get('vis-coords')
    my_model =SevenModel.objects.all().order_by('-id')[0]
    my_model.trn_coords = trn_coords
    mock_photo_url = os.path.join(media_root,my_model.vis.name)
    trans_img = four_point_transform(mock_photo_url, trn_coords)
    #save transformed image to model
    ret, buf = cv2.imencode('.jpg', trans_img) # cropped_image: cv2 / np array
    content = ContentFile(buf.tobytes())
    my_model.vis_trn.save('transformed vis.jpg', content)
    my_model.save()   
    #context
    full_grid_url = os.path.join(media_root,my_model.full_grid.name)
    context = {
        'my_model':my_model,
    }
    return render(request, 'lab/7-2b-2_vis_grid.html', context)

def strip_2b_3(request):
    x1 = float(request.POST.get('coordX1'))
    y1 = float(request.POST.get('coordY1'))
    x2 = float(request.POST.get('coordX2'))
    y2 = float(request.POST.get('coordY2'))
    canvas_width = float(request.POST.get('canvas_width'))
    canvas_height = float(request.POST.get('canvas_height'))
    my_coords = [x1,y1,x2,y2]
    my_model = SevenModel.objects.all().order_by('-id')[0]
    #context
    top = str(y1 * canvas_height) + 'px'
    height = str((y2-y1) * canvas_height) + 'px'
    left = str(x1 * canvas_width) + 'px'
    width = str((x2-x1) * canvas_width) + 'px'
    full_grid_url = os.path.join(media_root,my_model.full_grid.name)
    context = {
        'my_model':my_model,
        'full_grid_url':full_grid_url,
        'grid_name':my_model.full_grid.name,
        'top':top,
        'left':left,
        'width':width,
        'height':height,
        'se_left': str( (x1 * canvas_width) + ((x2-x1) * canvas_width) ) + 'px',
        'se_top': str(y1 * canvas_height)  + 'px',
    }
    return render(request, 'lab/7-2b-3_vis_adjust.html', context)

def strip_3(request):
    x1 = float(request.POST.get('coordX1'))
    y1 = float(request.POST.get('coordY1'))
    x2 = float(request.POST.get('coordX2'))
    y2 = float(request.POST.get('coordY2'))
    my_coords = [x1,y1,x2,y2]
    my_model = SevenModel.objects.all().order_by('-id')[0]
    my_model.mock_coords = my_coords
    my_model.save()
    full_grid_url = os.path.join(media_root,my_model.full_grid.name)
    context = {
        'my_model':my_model,
    }
    return render(request, 'lab/7-3_test_grid.html', context)

def strip_4(request):
    #save test_coords
    x1 = float(request.POST.get('coordX1'))
    y1 = float(request.POST.get('coordY1'))
    x2 = float(request.POST.get('coordX2'))
    y2 = float(request.POST.get('coordY2'))
    my_coords = [x1,y1,x2,y2]
    my_model = SevenModel.objects.all().order_by('-id')[0]
    my_model.test_coords = my_coords
    my_model.save()
    #crop image
    test_coords = my_coords
    test_x1 = test_coords[0]
    test_y1 = test_coords[1]
    test_x2 = test_coords[2]
    test_y2 = test_coords[3]
    try:
        my_url = os.path.join(media_root,my_model.test_image.name)
        image = Image.open(my_url)
    except:
        my_url = os.path.normpath(media_root+my_model.test_image.name)
        image = Image.open(my_url)
    width, height = image.size
    left = float(test_x1)*float(width)
    upper = float(test_y1)*float(height)
    right = float(test_x2)*float(width)
    lower = float(test_y2)*float(height)
    overlay_image_cropped = image.crop((left, upper, right, lower))
    #save cropped image
    my_path = os.path.join(media_root,'test_cropped.png')
    overlay_image_cropped.save(my_path)

    #make test strips 
    strip_request = strip_number(my_model.strip_request,my_model.first_col)
    graph_type_list = ['v' for i in range(len(strip_request))]

    #dev
    test_strips = stripper(my_path,graph_type_list,my_model.rows,my_model.cols,strip_request)

    #mock
    my_coords = ast.literal_eval(my_model.mock_coords)
    #crop image
    test_coords = my_coords
    test_x1 = test_coords[0]
    test_y1 = test_coords[1]
    test_x2 = test_coords[2]
    test_y2 = test_coords[3]
    try:
        my_url = os.path.join(media_root,my_model.mock_image.name)
        image = Image.open(my_url)
    except:
        my_url = os.path.normpath(media_root+my_model.mock_image.name)
        image = Image.open(my_url)
    width, height = image.size
    left = float(test_x1)*float(width)
    upper = float(test_y1)*float(height)
    right = float(test_x2)*float(width)
    lower = float(test_y2)*float(height)
    mock_image_cropped = image.crop((left, upper, right, lower))
    #save cropped image
    user_dir = os.path.join(seven_root, my_model.user_id)
    my_path = os.path.join(user_dir,'mock_cropped.png')
    mock_image_cropped.save(my_path)
    #graph type list for dens development
    #make test strips 
    mock_strips = stripper(my_path,graph_type_list,my_model.rows,my_model.cols,strip_request)

    #save strips to folder for pptx
    for i in range(len(test_strips)):
        my_filename = 'strip_' + str(i)+'.png'
        test_strips[i].save(os.path.join(user_dir,my_filename)) 

    for i in range(len(mock_strips)):
        my_filename = 'mock_strip_' + str(i)+'.png'
        mock_strips[i].save(os.path.join(user_dir,my_filename)) 

    #designing inclusion of densitometry
    graph_type_list = ['v' for i in range(len(test_strips))]
    make_pptx(test_strips,graph_type_list,strip_request,user_dir,my_model.user_id)

    return render(request, 'lab/7-4_result.html')

def strip_5(request):
    #Original error source: file_path=os.path.join('media','csv_array.csv')
    my_model = SevenModel.objects.all().order_by('-id')[0]
    pres_name = 'presentation_'+my_model.user_id+'.pptx'
    pres_path = os.path.join(my_model.user_id,pres_name)
    file_path = os.path.join(os.path.join(seven_root,pres_path))
    if os.path.exists(file_path): 
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/default")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

    raise Http404














def signal(request):
    form = SignalModelForm
    return render(request, 'lab/signal.html',{'form':form})

def signal_2(request):
   #Validate form and save model
    #my_model = SignalModel.objects.all().order_by('-id')[0]
    if request.method == 'POST':
        #form = SignalModelForm(request.POST, request.FILES, instance=my_model)
        form = SignalModelForm(request.POST, request.FILES)
        form.save()
        if form.is_valid():
            form.save()
    else:
        print('NOT VALID')

    my_model = SignalModel.objects.all().order_by('-id')[0]
    #generate grid file
    rows = my_model.rows
    cols = my_model.cols
    grid_unit_path = os.path.join(lab_static_root, 'grid-unit.png')
    full_grid = generate_grid(rows,cols,grid_unit_path)

    #save full grid to model
    ret, buf = cv2.imencode('.png', full_grid) 
    content = ContentFile(buf.tobytes())
    my_model.full_grid.save('full_grid.png', content)
    my_model.save()    
    context = {
        'my_model':my_model,
    }
    return render(request, "lab/signal_2.html", context)


def signal_3(request):

    x1 = float(request.POST.get('coordX1'))
    y1 = float(request.POST.get('coordY1'))
    x2 = float(request.POST.get('coordX2'))
    y2 = float(request.POST.get('coordY2'))
    my_coords = [x1,y1,x2,y2]

    my_model = SignalModel.objects.all().order_by('-id')[0]
    my_model.crop_coords = my_coords
    my_model.save()

    test_coords = my_coords
    test_x1 = test_coords[0]
    test_y1 = test_coords[1]
    test_x2 = test_coords[2]
    test_y2 = test_coords[3]

    #crop image
    my_url = os.path.join(media_root,my_model.img.name)
    image = Image.open(my_url)

    width, height = image.size

    left = float(test_x1)*float(width)
    upper = float(test_y1)*float(height)
    right = float(test_x2)*float(width)
    lower = float(test_y2)*float(height)

    overlay_image_cropped = image.crop((left, upper, right, lower))

    #convert PIL to openCV
    open_cv_image = numpy.array(overlay_image_cropped) 
    # Convert RGB to BGR 
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

    #save cropped_image to model
    ret, buf = cv2.imencode('.png', open_cv_image) 
    content = ContentFile(buf.tobytes())
    my_model.img_crop.save('cropped.png', content)
    my_model.save()    
    
    #make slice list
    rows = my_model.rows
    cols = my_model.cols
    slice_list = slice_to_list(overlay_image_cropped, rows, cols)

    #NEED TO MELT THE SLICE LIST, AS CSV WRITES IN ROWS, NOT COLS
    format_list = []
    c=0
    r=0
    for i in range(rows):
        for i in range(cols):
            format_list.append(slice_list[c+r])
            c+=rows
        r+=1
        c=0

    #crop each image in list and measure darkness
    mask = make_mask(200)
    
    #measure darknesses
    darkness_list = []
    my_row = []

    c = 0
    for row in range(rows):
        for col in range(cols):
            cropped = circle_crop(format_list[c],mask)
            my_row.append(measure_darkness(cropped))
            c += 1
        darkness_list.append(my_row)
        my_row = []

    my_model.dens_list = darkness_list
    my_model.save()

    path_name = os.path.join('media','signal') #!!!!!!!!!!!!!! Python anywhere problem
    path_name = os.path.join(path_name,'signal.csv')

    with open(path_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(darkness_list)

    #add form for strip requests
    form = SignalModelForm2(instance = my_model)

    return render(request, 'lab/signal_3.html', {'my_model':my_model,'form':form})

def signal_4(request):
    #Original error source: file_path=os.path.join('media','csv_array.csv')
    file_path=os.path.join(media_root,'signal')
    file_path=os.path.join(file_path,'signal.csv')

    if os.path.exists(file_path): #!!!!!!!!!!!!!!!!!

        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/default")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

    raise Http404

def signal_5(request): #save form and make next templates. 
    #Validate form and save model
    my_model = SignalModel.objects.all().order_by('-id')[0]
    if request.method == 'POST':

        form = SignalModelForm2(request.POST, request.FILES,instance=my_model)
        if form.is_valid():
            form.save()
    my_model.save()

    strip_list = my_model.strip_request.split(',')
    context = {'my_model':my_model,'strip_list':strip_list}
    return render(request, 'lab/signal_5.html', context)

def signal_6(request):
    #update model instance from forms
    #graph types
    my_model = SignalModel.objects.all().order_by('-id')[0]
    graph_types = []
    for i in range(len(my_model.strip_request.split(','))):
        graph_types.append(request.POST.get(str(i+1)))
    my_model.graph_types = graph_types
    my_model.save()

    #make list of spot darknesses from strip
    strip_request = strip_number(my_model.strip_request,my_model.first_col)    
    dens_list = ast.literal_eval(my_model.dens_list)
    dens_list = [x for xs in dens_list for x in xs]
    my_row = []
    my_x = []
    for strip in strip_request:
        for i in range(strip[0]-1,strip[1]-1):
            my_row.append(dens_list[i])
        my_x.append(my_row)
        my_row = []
 
    return render(request, 'lab/signal_6.html')














def sd_upload(request):
    #make new instance and set user_id as four digit number
    #generate id
    this_now = datetime.now()
    hash = this_now.strftime("%Y-%m-%d-%H-%M-%S")
    my_model = SDModel(user_id=hash)
    my_model.save() 

    #load form of that existing instance
    sd_form = SDModelForm(instance = my_model)
    return render(request, 'lab/sd_upload.html',{'form':sd_form})


def sd_validate(request):
    my_model = SDModel.objects.all().order_by('-id')[0]

    #Validate form and save model
    if request.method == 'POST':
        form = SDModelForm(request.POST, request.FILES,  instance=my_model)
        if form.is_valid():
            form.save()
    else:
        args={}
        form = SDModelForm()
        args['sd_form'] = form
        return render(request, 'lab/sd_upload.html',args)

    #convert strip_request to usable list
    my_model.strip_request = strip_number(my_model.strip_request,my_model.first_col)
    my_model.save()

    #format graph_types
    my_string = my_model.graph_types
    my_string.replace(' ','')
    my_list = my_string.split(',')
    my_model.graph_types = my_list
    #format graph types if discovery array - y axes need to be kept the same if discovery array
    if 'd' in my_list:
        new_list = []
        for i in range(len(my_model.strip_request)):
            new_list.append('d')
        my_model.graph_types = new_list
    my_model.save()

    #generate grid file
    rows = 20
    cols = my_model.cols
    grid_unit_path = os.path.join(lab_static_root, 'grid-unit.png')
    full_grid = generate_grid(rows,cols,grid_unit_path)
    #save full grid to model
    ret, buf = cv2.imencode('.png', full_grid) 
    content = ContentFile(buf.tobytes())
    my_model.full_grid.save('full_grid.png', content)   

    return redirect('lab:sd_redirect') 

def sd_redirect(request):
    my_model = SDModel.objects.all().order_by('-id')[0]
    c = ast.literal_eval(my_model.config)['c']

    if c == 0:
        my_model.config = "{'c':1}"
        my_model.save()
        header = 'Test Array'
        context = {'my_model':my_model,'img':my_model.img_1,'header':header}
        return render(request, 'lab/sd_master.html',context) 

    elif c == 1:
        #save coords
        x1 = float(request.POST.get('coordX1'))
        y1 = float(request.POST.get('coordY1'))
        x2 = float(request.POST.get('coordX2'))
        y2 = float(request.POST.get('coordY2'))
        my_coords = [x1,y1,x2,y2]
        my_model.img_1_coords = my_coords

        #update counter
        my_model.config = "{'c':2}"
        my_model.save()

        header = 'Control Array'
        context = {'my_model':my_model,'img':my_model.img_2,'header':header}
        return render(request, 'lab/sd_master.html',context) 

    elif c == 2:
        x1 = float(request.POST.get('coordX1'))
        y1 = float(request.POST.get('coordY1'))
        x2 = float(request.POST.get('coordX2'))
        y2 = float(request.POST.get('coordY2'))
        my_coords = [x1,y1,x2,y2]
        my_model.img_2_coords = my_coords
        my_model.save()
        return redirect('lab:sd_result')


def sd_result(request):
    my_model = SDModel.objects.all().order_by('-id')[0]

    #crop img1
    test_coords = ast.literal_eval(my_model.img_1_coords)
    my_x1, my_y1, my_x2, my_y2 = test_coords[0],test_coords[1],test_coords[2],test_coords[3]
    try:
        my_url = os.path.join(media_root,my_model.img_1.name)
        image = Image.open(my_url)
    except:
        my_url = os.path.normpath(media_root+my_model.img_1.name)
        image = Image.open(my_url)
    width, height = image.size
    left = float(my_x1)*float(width)
    upper = float(my_y1)*float(height)
    right = float(my_x2)*float(width)
    lower = float(my_y2)*float(height)
    img_1_cropped = image.crop((left, upper, right, lower))
    #save cropped image
    #convert PIL to openCV
    open_cv_image = numpy.array(img_1_cropped) 
    # Convert RGB to BGR 
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
    #save cropped_image to model
    ret, buf = cv2.imencode('.png', open_cv_image) 
    content = ContentFile(buf.tobytes())
    my_model.img_1_crop.save('img_1_cropped.png', content)
    #my_model.save()    

    #crop img2
    test_coords = ast.literal_eval(my_model.img_2_coords)
    my_x1, my_y1, my_x2, my_y2 = test_coords[0],test_coords[1],test_coords[2],test_coords[3]
    try:
        my_url = os.path.join(media_root,my_model.img_2.name)
        image = Image.open(my_url)
    except:
        my_url = os.path.normpath(media_root+my_model.img_2.name)
        image = Image.open(my_url)
    width, height = image.size
    left = float(my_x1)*float(width)
    upper = float(my_y1)*float(height)
    right = float(my_x2)*float(width)
    lower = float(my_y2)*float(height)
    img_2_cropped = image.crop((left, upper, right, lower))
    #save cropped image
    #convert PIL to openCV
    open_cv_image = numpy.array(img_2_cropped) 
    # Convert RGB to BGR 
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
    #save cropped_image to model
    ret, buf = cv2.imencode('.png', open_cv_image) 
    content = ContentFile(buf.tobytes())
    my_model.img_2_crop.save('img_2_cropped.png', content)

    my_model.save()    



    ### Measure Darkness and save to csv files ###

    #get darkness list of img1
    rows = 20
    cols = my_model.cols
    slice_list = slice_to_list(img_1_cropped, rows, cols)

    #NEED TO MELT THE SLICE LIST, AS CSV WRITES IN ROWS, NOT COLS
    format_list = []
    c=0
    r=0
    for i in range(rows):
        for i in range(cols):
            format_list.append(slice_list[c+r])
            c+=rows
        r+=1
        c=0

    #crop each image in list and measure darkness
    mask = make_mask(200)
    
    #measure darknesses
    darkness_list_img1 = []
    my_row = []

    c = 0
    for row in range(rows):
        for col in range(cols):
            cropped = circle_crop(format_list[c],mask)
            my_row.append(measure_darkness(cropped))
            c += 1
        darkness_list_img1.append(my_row)
        my_row = []


    #get darkness list of img2
    rows = 20
    cols = my_model.cols
    slice_list = slice_to_list(img_2_cropped, rows, cols)

    #NEED TO MELT THE SLICE LIST, AS CSV WRITES IN ROWS, NOT COLS
    format_list = []
    c=0
    r=0
    for i in range(rows):
        for i in range(cols):
            format_list.append(slice_list[c+r])
            c+=rows
        r+=1
        c=0

    #crop each image in list and measure darkness
    mask = make_mask(200)
    
    #measure darknesses
    darkness_list_img2 = []
    my_row = []

    c = 0
    for row in range(rows):
        for col in range(cols):
            cropped = circle_crop(format_list[c],mask)
            my_row.append(measure_darkness(cropped))
            c += 1
        darkness_list_img2.append(my_row)
        my_row = []


    #calculate min, max and delta for darkness transformation
    darkness_list_values = [] 
    if my_model.norm == True:
        for row in range(rows):
            for col in range(cols):
                darkness_list_values.append(darkness_list_img1[row][col])
                darkness_list_values.append(darkness_list_img2[row][col])
    else:
        #just normalise to test array max for darkness transformation
        for row in range(rows):
            for col in range(cols):
                darkness_list_values.append(darkness_list_img1[row][col])
    my_min = min_(darkness_list_values)
    my_max = max_(darkness_list_values)
    my_delta =  my_max-my_min


    #transform data so that values increase from light to dark
    darkness_list_img_1_trn = []
    my_row = []
    for row in range(rows):
        for col in range(cols):
            #invert value while retaining distance from 0
            my_row.append(
                ((1-((darkness_list_img1[row][col]-my_min)/my_delta))*my_delta)+my_min
            )
        darkness_list_img_1_trn.append(my_row)
        my_row = []

    #export for making graphs
    #if norm = false, then this will be fed to graph
    my_model.dens_list = darkness_list_img_1_trn
    my_model.save()

    darkness_list_img_2_trn = []
    my_row = []
    for row in range(rows):
        for col in range(cols):
            #invert value while retaining distance from 0
            my_row.append(
                ((1-((darkness_list_img2[row][col]-my_min)/my_delta))*my_delta)+my_min
            )
        darkness_list_img_2_trn.append(my_row)
        my_row = []


    #save test image darknesses
    path_name = os.path.join(media_root,'sd') #!!!!!!!!!!!!!! Python anywhere problem
    path_name = os.path.join(path_name,my_model.user_id) 
    path_name = os.path.join(path_name,'img_1.csv')

    with open(path_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(darkness_list_img_1_trn)
    #save control image darknesses
    if my_model.norm == True:
        path_name = os.path.join(media_root,'sd') #!!!!!!!!!!!!!! Python anywhere problem
        path_name = os.path.join(path_name,my_model.user_id) 
        path_name = os.path.join(path_name,'img_2.csv')

        with open(path_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(darkness_list_img_2_trn)

    #background subtract 
    if my_model.norm == True:
        my_row = []
        darkness_list_background_subtracted = []
        for row in range(rows):
            for col in range(cols):
                my_row.append(darkness_list_img_1_trn[row][col] - darkness_list_img_2_trn[row][col])
            darkness_list_background_subtracted.append(my_row)
            my_row = []

        #save normalised data
        path_name = os.path.join(media_root,'sd') #!!!!!!!!!!!!!! Python anywhere problem
        path_name = os.path.join(path_name,my_model.user_id) 
        path_name = os.path.join(path_name,'background_subtracted_data.csv')

        with open(path_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(darkness_list_background_subtracted)

        #export for making graphs
        my_model.dens_list = darkness_list_background_subtracted
        my_model.save()




    graph_types = ast.literal_eval(my_model.graph_types)
    strip_request = ast.literal_eval(my_model.strip_request)

    test_strips = stripper2(
        my_model.img_1_crop,graph_types,rows,cols,
        strip_request
        )
    mock_strips = stripper2(
        my_model.img_2_crop,graph_types,rows,cols,strip_request
        )


    my_dir = os.path.join(media_root,'sd') #!!!!!!!!!!!!!! Python anywhere problem
    my_dir = os.path.join(my_dir,my_model.user_id) 

    #save strips to folder for pptx
    for i in range(len(test_strips)):
        my_filename = 'strip_' + str(i)+'.png'
        test_strips[i].save(os.path.join(my_dir,my_filename)) 

    for i in range(len(mock_strips)):
        my_filename = 'mock_strip_' + str(i)+'.png'
        mock_strips[i].save(os.path.join(my_dir,my_filename)) 

    #quick patch for to accomodate disc_y_lim
    graph_types_dummy = graph_types
    if 'd' in graph_types:
        graph_types_dummy = []
        for i in range(len(strip_request)):
            graph_types_dummy.append('h')

    make_pptx(
        test_strips,graph_types_dummy,strip_request,my_dir,my_model.user_id
    )


    ### GRAPHS ###
    dens_list = my_model.dens_list
    #convert dens_list which is in array format to flat list of intensities to match strip_request indices
    dens_list_flat = []
    for col in range(cols):
        for row in range(rows):
            dens_list_flat.append(dens_list[row][col])

    #make graphs

    #disc array - calculate mx value from selected slice darknesses for y axis
    if 'd' in graph_types:
        #function to round max to nearest number of choice
        def myround20(x, base=20):
            return base * round((x+1)/base)

        my_flat_list = []
        for i in range(len(strip_request)):
            #convert strip request into slice indices
            new_strip = []
            new_strip.append(strip_request[i][0]-1)
            new_strip.append(strip_request[i][1])
            for i in dens_list_flat[new_strip[0]:new_strip[1]]:
                my_flat_list.append(i)
        disc_y_max = myround20(max_(my_flat_list))

        #return to v so graphs are made
        graph_types = []
        for i in range(len(strip_request)):
            graph_types.append('h')
    else:
        disc_y_max = False

    for i in range(len(strip_request)):
        #convert strip request into slice indices
        new_strip = []
        new_strip.append(strip_request[i][0]-1)
        new_strip.append(strip_request[i][1])

        my_heights = dens_list_flat[new_strip[0]:new_strip[1]]

        my_x = [j for j in range(len(my_heights))]
        my_filename = 'graph_'+str(i)
        if graph_types[i] == 'h':
            h_bar(my_x,my_heights,my_dir,my_filename,disc_y_max)
        if graph_types[i] == 'v':
            v_bar(my_x,my_heights,my_dir,my_filename,disc_y_max)


    #open ppt
    my_dir = os.path.join(media_root,'sd') #!!!!!!!!!!!!!! Python anywhere problem
    my_dir = os.path.join(my_dir,my_model.user_id) 
    my_filename = 'presentation_'+my_model.user_id+'.pptx'
    my_dir = os.path.join(my_dir,my_filename)

    #add graphs to ppt
    if my_dir == 'blank':
        prs = Presentation()
        prs.slide_width = Cm(33.9)
        prs.slide_height = Cm(19.1)
        for i in range(len(strip_request)):
            slide = prs.slides.add_slide(prs.slide_layouts[0])
    else:
        prs = Presentation(my_dir)
    
    h_left = Cm(8.7)
    h_top = Cm(2.2)
    v_left = Cm(8.4)
    v_top = Cm(6.5)
    #width = Cm(0.7)
    
    slides_list = [slide.slide_id for slide in prs.slides]

    for i in range(len(strip_request)):
        slide = prs.slides.get(slides_list[i])

        #get path to graph
        my_dir = os.path.join(media_root,'sd') #!!!!!!!!!!!!!! Python anywhere problem
        my_dir = os.path.join(my_dir,my_model.user_id) 
        my_filename = "graph_"+str(i)+".png"
        my_dir = os.path.join(my_dir,my_filename)

        if graph_types[i] == "h":
            img = slide.shapes.add_picture(my_dir,h_left,h_top)
        if graph_types[i] == "v":
            img = slide.shapes.add_picture(my_dir,v_left,v_top)

    #save ppt
    my_dir = os.path.join(media_root,'sd') #!!!!!!!!!!!!!! Python anywhere problem
    my_dir = os.path.join(my_dir,my_model.user_id) 
    my_filename = 'presentation_'+my_model.user_id+'.pptx'
    my_dir = os.path.join(my_dir,my_filename)
    prs.save(my_dir)

    #compress files for output
    files_to_compress = []
    compression_filenames = []
    my_dir = os.path.join(media_root,'sd') #!!!!!!!!!!!!!! Python anywhere problem
    my_dir = os.path.join(my_dir,my_model.user_id) 
    for i in range(len(strip_request)):

        my_filename = 'graph_'+str(i)+'.png'
        files_to_compress.append(os.path.join(my_dir,my_filename))
        compression_filenames.append(my_filename)

        my_filename = 'strip_'+str(i)+'.png'
        files_to_compress.append(os.path.join(my_dir,my_filename))
        compression_filenames.append(my_filename)

        files_to_compress.append(os.path.join(my_dir,'img_1.csv'))
        compression_filenames.append('img_1.csv')
        files_to_compress.append(os.path.join(my_dir,'img_2.csv'))
        compression_filenames.append('img_2.csv')
        files_to_compress.append(os.path.join(my_dir,'background_subtracted_data.csv'))
        compression_filenames.append('background_subtracted_data.csv')

        my_filename = 'presentation_'+my_model.user_id+'.pptx'
        files_to_compress.append(os.path.join(my_dir,my_filename))
        compression_filenames.append('DATA POWERPOINT.pptx')

    file_compress(files_to_compress,compression_filenames,os.path.join(my_dir,'data_peptide_array.zip'))


    return render(request, 'lab/sd_result.html')



def sd_download(request):
    my_model = SDModel.objects.all().order_by('-id')[0]
    my_dir = os.path.join(media_root,'sd') #!!!!!!!!!!!!!! Python anywhere problem
    my_dir = os.path.join(my_dir,my_model.user_id)
    file_path = os.path.join(my_dir,'data_peptide_array.zip')

    if os.path.exists(file_path): 

        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/default")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

    raise Http404