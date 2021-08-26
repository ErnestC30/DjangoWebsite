from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import Profile

class Media(models.Model):
    title = models.CharField(max_length=50)
    media = models.FileField(upload_to='uploads')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, default='image')
    description = models.TextField()

class Post(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    posted_to = models.ForeignKey(Media, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content

