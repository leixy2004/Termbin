from django.db import models
import uuid,hashlib

from django.urls import reverse

class User(models.Model):
    username=models.CharField(max_length=50)
    password_sha256=models.CharField(max_length=70)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    def set_password(self,password):
        self.password_sha256=hashlib.sha256((password+"JeSuisAnakin222").encode()).hexdigest()
    def check_password(self,password):
        return self.password_sha256==hashlib.sha256((password+"JeSuisAnakin222").encode()).hexdigest()

# Create your models here.
class Paste(models.Model):
    paste_text = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    paste_digest = models.CharField(max_length=70)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    short_id = models.CharField(max_length=4)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.paste_text
    def get_absolute_url(self):
        return reverse("short-detail", args=[str(self.short_id),])
    