from django.db import models
from django.conf import settings

class Template(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100) # From the predefined list in index.html
    file = models.FileField(upload_to='templates/') # Store in MEDIA_ROOT/templates/
    description = models.TextField(blank=True, null=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
