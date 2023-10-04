from django.shortcuts import render
from django.http import HttpResponse,HttpRequest, Http404
from .models import Paste
# Create your views here.
def index(request : HttpRequest):
    if request.method == "POST":
        text = request.body
        text=text[text.find(b'\r\n',text.find(b'\r\n',text.find(b'\r\n')+1)+1)
                  :text.rfind(b'\r\n',0,text.rfind(b'\r\n')-1)]
        text=text.strip(b'\r\n')
        paste=Paste(paste_text=text.decode(),paste_digest=hash(text))
        paste.save()
    return HttpResponse("Here is INDEX.")

def detail(request,paste_uuid):
    try:
        paste = Paste.objects.get(pk=paste_uuid)
    except Paste.DoesNotExist:
        raise Http404("No paste here.")
    return HttpResponse(paste)