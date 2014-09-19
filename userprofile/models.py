# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


class InterestTag(models.Model):
    tag_name = models.CharField(max_length=25)

    def __str__(self):
        return self.tag_name


class Profile(models.Model):
    """
    The user profile model that extends the user model with a OneToOne link
    """

    def default_profile_picture():  # TODO: Así se define una función acá dentro del modelo?
        return "default.jpg"

    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='user_avatars', default=default_profile_picture())     # TODO: asco Default. No funciona con lambda
    bio = models.CharField(max_length=200)  # TODO: De qué manera obligaría a completar esto cuando se crea el usuario?
    interest_tags = models.ManyToManyField(InterestTag, related_name='users', blank=True)

    def __str__(self):
        return self.user.username