from django.db import models
from django.contrib.auth.models import User
from PIL import Image

DEFAULT_IMAGE = 'default_thumbnail.jpg'

class Profile(models.Model):
    """Extension of default User model.
       Adds a profile image and description."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default=DEFAULT_IMAGE, upload_to='profile_pics')
    description = models.TextField(default='Add description here.')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """Decrease the image size for user profile."""
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)