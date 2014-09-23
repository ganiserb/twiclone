# coding=utf-8
from django.db import models
import users.models

class User(users.models.User):
    """
    Extends the user model for the project adding user specific settings about the content
    """
    PUBLIC = 'PU'       # Everyone can see
    FOLLOWING = 'FI'    # Only those i'm following can see

    VISIBILITY_CHOICES = (
        (PUBLIC, 'Public'),
        (FOLLOWING, 'Those I follow'),
    )

    visibility = models.CharField(max_length=2,
                                  choices=VISIBILITY_CHOICES,
                                  default=PUBLIC)

    twicles_per_page = models.PositiveSmallIntegerField(default=10)

class Twicle(models.Model):
    """
    Represents a post by the user. May include a picture
    """
    text = models.CharField(max_length=200)
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="twiclo_images", null=True)

    def __str__(self):
        return self.text
