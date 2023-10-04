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
        # return HttpResponse("date:",paste.pub_date,
        #                     "\ndigest:",paste.paste_digest,
        #                     "\nsize:",paste.paste_text.len(),
        #                     "\nurl:",paste.get_absolute_url())
        response="Date:%s\r\nDigest:%s\r\nSize:%d\r\nUrl:\r\n"%(str(paste.pub_date),
                                                                  paste.paste_digest,
                                                                  len(paste.paste_text))
        return HttpResponse(response)
    return HttpResponse("Here is INDEX.")

def detail(request,paste_uuid):
    try:
        paste = Paste.objects.get(pk=paste_uuid)
    except Paste.DoesNotExist:
        raise Http404("No paste here.")
    return HttpResponse(paste)