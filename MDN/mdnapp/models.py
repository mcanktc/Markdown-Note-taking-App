from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def user_directory_path(instance, filename):
    return f'notes/user_{instance.author.id}/note_{instance.pk or "new"}.md'

class Note(models.Model):
    NOTE_OPTIONS = [
        ('T', 'text'),
        ('F', 'file'),
    ]
    title = models.CharField(max_length=225)
    text = models.CharField(max_length=2500, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    md_file = models.FileField(upload_to=user_directory_path, blank=True)
    take_type = models.CharField(max_length=1, choices=NOTE_OPTIONS)

    def __str__(self):
        return self.title
    

