from django.shortcuts import render
from lab.seq_studies import *

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