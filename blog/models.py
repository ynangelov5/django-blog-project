from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from blog.mixins import Timestamps 


class Post(Timestamps):
    title = models.CharField(
        max_length=100, 
        validators=[MinLengthValidator(2)]
        )
    content = models.TextField()
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="posts"
        )

    def __str__(self):
        return self.title
    


