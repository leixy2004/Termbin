from django.db import models
import uuid

from django.urls import reverse
# Create your models here.
class Paste(models.Model):
    paste_text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    paste_digest = models.CharField(max_length=200)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})
    def __str__(self) -> str:
        return self.paste_text
