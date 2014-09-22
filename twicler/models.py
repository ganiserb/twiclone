# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


class Twiclo(models.Model):
    # TODO: Describir qué es cada modelo
    text = models.CharField(max_length=200)
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="twiclo_images", null=True)

    def __str__(self):
        return self.text


class UserSettings(models.Model):
    PUBLIC = 'PU'       # Everyone can see
    FOLLOWING = 'FI'    # Only those i'm following can see

    VISIBILITY_CHOICES = (
        (PUBLIC, 'Public'),
        (FOLLOWING, 'Those I follow'),
    )

    user = models.OneToOneField(User)
    visibility = models.CharField(max_length=2,
                                  choices=VISIBILITY_CHOICES,
                                  default=PUBLIC)

    following = models.ManyToManyField('self')
    followers = models.ManyToManyField('self')

    twicles_per_page = models.PositiveSmallIntegerField(default=10)