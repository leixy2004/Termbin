from django.db import models
import uuid

from django.urls import reverse
# Create your models here.
class Paste(models.Model):
    paste_text = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    paste_digest = models.CharField(max_length=50)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    short_id = models.CharField(max_length=4)
    def __str__(self) -> str:
        return self.paste_text
    def get_absolute_url(self):
        return reverse("short-detail", args=[str(self.short_id),])
    