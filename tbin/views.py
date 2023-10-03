from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Paste
# Create your views here.
def index(request):
    return HttpResponse("Here is INDEX.")

def detail(request,paste_uuid):
    try:
        paste = Paste.objects.get(pk=paste_uuid)
    except Paste.DoesNotExist:
        raise Http404("No paste here.")
    return HttpResponse(paste)