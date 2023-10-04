from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
from .models import Paste
import hashlib

def clean_body(text : bytes):
    return text[text.find(b'\r\n',text.find(b'\r\n',text.find(b'\r\n')+1)+1)
                  :text.rfind(b'\r\n',0,text.rfind(b'\r\n')-1)].strip(b'\r\n').decode()+"\n"

# Create your views here.
def index(request : HttpRequest):
    if request.method == "POST":
        text=clean_body(request.body)
        hash_text=hashlib.sha256(text.encode())
        paste=Paste(paste_text=text,paste_digest=hash_text.hexdigest())
        # print(paste.id)
        for t in str(paste.id).split('-')[1:-1]:
            if Paste.objects.filter(short_id=t).count() == 0:
                paste.short_id=t
                break
            print("WRONG")
        paste.save()
        response="Date: %s\r\nDigest: %s\r\nUUID: %s\r\nShort: %s\r\nSize: %d\r\nUrl: %s\r\n" %(str(paste.pub_date),paste.paste_digest,paste.id,paste.short_id,len(paste.paste_text),request.build_absolute_uri(paste.get_absolute_url()))
        return HttpResponse(response)
    return HttpResponse("Here is INDEX.")

def detail(request:HttpRequest,paste_uuid):
    try:
        paste = Paste.objects.get(pk=paste_uuid)
    except Paste.DoesNotExist:
        return HttpResponse("No paste here.")
    if request.method == "DELETE":
        paste.delete()
        return HttpResponse(str(paste_uuid)+" Deleted.")
    if request.method == "PUT":
        text = clean_body(request.body)
        paste.paste_text=text
        paste.paste_digest=hashlib.sha256(paste.paste_text.encode()).hexdigest()
        paste.save()
        return HttpResponse(str(paste_uuid)+" Modified.")
    return HttpResponse(paste)

def detail_by_short(request:HttpRequest, short_id):
    try:
        paste = Paste.objects.get(short_id=short_id)
    except Paste.DoesNotExist:
        return HttpResponse("No paste here.")
    if request.method == "DELETE":
        paste.delete()
        return HttpResponse(str(short_id)+" Deleted.")
    if request.method == "PUT":
        text = clean_body(request.body)
        paste.paste_text=text
        paste.paste_digest=hashlib.sha256(paste.paste_text.encode()).hexdigest()
        paste.save()
        return HttpResponse(str(short_id)+" Modified.")
    return HttpResponse(paste)