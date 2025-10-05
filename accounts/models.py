from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE
        )
    image = models.ImageField(
        default='common/default_profile_pic.jpg',
        upload_to='profile_pics'
        )
    bio = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        max_size = (300, 300)

        if img.width > max_size[0] or img.height > max_size[1]:
            img.thumbnail(max_size)
            img.save(self.image.path)
    
