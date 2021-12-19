from django.shortcuts import render

# Create your views here.
def resources(request):
    return render(request, 'lab/resources.html')