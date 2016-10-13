from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    context_dict = {'boldmessage': "Crunchy, fresh, light, cheese pizza!"}
    return render(request, 'netchan/index.html', context=context_dict)

def about(request):
    return render(request, 'netchan/about.html')