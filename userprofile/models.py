# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


class InterestTag(models.Model):
    tag_name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.tag_name


class Profile(models.Model):    # TODO: Extender el modelo de auth
    """
    The user profile model that extends the user model with a OneToOne link
    """

    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='user_avatars', default="default.jpg")
    bio = models.CharField(max_length=200)  # TODO: De qué manera obligaría a completar esto cuando se crea el usuario? -> Extendiendo auth.user
    interest_tags = models.ManyToManyField(InterestTag, related_name='users', blank=True)

    def __str__(self):
        return self.user.username