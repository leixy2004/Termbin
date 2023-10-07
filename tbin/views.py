from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
from .models import Paste,User
import hashlib

def __clean_body(text : bytes):
    return text[text.find(b'\r\n',text.find(b'\r\n',text.find(b'\r\n')+1)+1)
                  :text.rfind(b'\r\n',0,text.rfind(b'\r\n')-1)].strip(b'\r\n').decode()+"\n"

# Create your views here.
def index(request : HttpRequest):
    if request.method == "POST":
        text=__clean_body(request.body)
        hash_text=hashlib.sha256(text.encode())
        paste=Paste(paste_text=text,paste_digest=hash_text.hexdigest())
        for t in str(paste.id).split('-')[1:-1]:
            if Paste.objects.filter(short_id=t).count() == 0:
                paste.short_id=t
                break
            print("WRONG")
        paste.save()
        response="Date: %s\r\nDigest: %s\r\nUUID: %s\r\nShort: %s\r\nSize: %d\r\nUrl: %s\r\n" %(str(paste.pub_date),paste.paste_digest,paste.id,paste.short_id,len(paste.paste_text),request.build_absolute_uri(paste.get_absolute_url()))
        if "user_uuid" in request.session:
            try:
                paste.author=User.objects.get(pk=request.session["user_uuid"])
                paste.save()
                response+="Author: %s\r\n" % paste.author.username
            except KeyError:
                print("WRONG")
            
        return HttpResponse(response)
    # GET
    if "user_uuid" in request.session:
        try:
            user=User.objects.get(pk=request.session["user_uuid"])
        except User.DoesNotExist:
            return HttpResponse("Dangerous ERROR!")
        return HttpResponse("Welcome,%s! Here is INDEX." % user.username)
    return HttpResponse("Here is INDEX.")
    # print(request.session["user_uuid"])


def detail(request:HttpRequest,paste_uuid):
    try:
        paste = Paste.objects.get(pk=paste_uuid)
    except Paste.DoesNotExist:
        return HttpResponse("No paste here.")
    if paste.view_limited:
        if "user_uuid" in request.session:
            try:
                user=User.objects.get(pk=request.session["user_uuid"])
            except User.DoesNotExist:
                return HttpResponse("Dangerous ERROR!")
            if user not in paste.acceptable_viewer.all():
                return HttpResponse("You are blocked out in this paste.")
        else:
            return HttpResponse("You are blocked out in this paste.")
        
    if request.method == "DELETE":
        paste.delete()
        return HttpResponse(str(paste_uuid)+" Deleted.")
    if request.method == "PUT":
        text = __clean_body(request.body)
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
    if paste.view_limited:
        if "user_uuid" in request.session:
            try:
                user=User.objects.get(pk=request.session["user_uuid"])
            except User.DoesNotExist:
                return HttpResponse("Dangerous ERROR!")
            if user not in paste.acceptable_viewer.all():
                return HttpResponse("You are blocked out in this paste.")
        else:
            return HttpResponse("You are blocked out in this paste.")
    if request.method == "DELETE":
        paste.delete()
        return HttpResponse(str(short_id)+" Deleted.")
    if request.method == "PUT":
        text = __clean_body(request.body)
        paste.paste_text=text
        paste.paste_digest=hashlib.sha256(paste.paste_text.encode()).hexdigest()
        paste.save()
        return HttpResponse(str(short_id)+" Modified.")
    return HttpResponse(paste)

def register(request : HttpRequest):
    # print(request.body)
    try:
        name=request.POST.get("name")
        password=request.POST.get("password")
    except KeyError:
        return HttpResponse("ERROR")
    # print(name,password)
    if (User.objects.filter(username=name).count()):
        return HttpResponse("The name has been used.")
    user=User(username=name)    
    user.set_password(password=password)
    user.save()
    return HttpResponse("User %s has been created successfully." % user.username)

def login(request : HttpRequest):
    if "user_uuid" in request.session:
        return HttpResponse("You had been logged in!")
    if request.method=="POST":
        try:
            user=User.objects.get(username=request.POST["name"])
        except User.DoesNotExist:
            return HttpResponse("There is not such user.")
    
        if (user.check_password(request.POST["password"])):
            request.session["user_uuid"]=str(user.id)
            return HttpResponse("Welcome, %s!" % user.username)
        else:
            return HttpResponse("Login failed. Please try again.")
    return HttpResponse("Please use \"-d \"name=...&password=...\"\" to login.")
    
def logout(request : HttpRequest):
    try:
        del request.session["user_uuid"]
    except KeyError:
        return HttpResponse("You had been logged out already.")
    return HttpResponse("You are logged out successfully.")

def make_private(request: HttpRequest,paste_uuid):
    if "user_uuid" in request.session:
        try:
            user=User.objects.get(pk=request.session["user_uuid"])
        except User.DoesNotExist:
            return HttpResponse("Dangerous ERROR!")
        try:
            paste = Paste.objects.get(pk=paste_uuid)
        except Paste.DoesNotExist:
            return HttpResponse("No paste here.")
        if not paste.author or paste.author.id!=user.id:
            return HttpResponse("The paste does not belong to you.")
        paste.view_limited=True
        paste.acceptable_viewer.add(user)
        paste.save()
        return HttpResponse("Successful.")
    return HttpResponse("Not logged in yet.")

def add_viewer(request: HttpRequest):
    pass