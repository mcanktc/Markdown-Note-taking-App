from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def note_file_upload_path(instance, filename):
    return f'notes/user_{instance.owner.id}/{filename}'

class Note(models.Model):
    title = models.CharField(max_length=225)
    content = models.TextField(max_length=5000, blank=True)
    file = models.FileField(upload_to=note_file_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')

    def __str__(self):
        return self.title