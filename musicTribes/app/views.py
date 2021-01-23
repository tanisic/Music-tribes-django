from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request,"app/index.html",None)

def tribe(request):
    return render(request,"app/tribe.html",None)