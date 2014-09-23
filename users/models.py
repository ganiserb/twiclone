# coding=utf-8
from django.db import models
import django.contrib.auth.models


class InterestTag(models.Model):
    tag_name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.tag_name


class User(django.contrib.auth.models.User):
    """
    This extends the built-in user model
    """
    avatar = models.ImageField(upload_to='user_avatars', default="default.jpg")
    bio = models.CharField(max_length=200)

    interest_tags = models.ManyToManyField(InterestTag, related_name='users_interested', blank=True)

    following = models.ManyToManyField("self", symmetrical=False, related_name="followed_by")  # QUESTION: symetrical = False? En True implica que si yo sigo a alguien él me sigue a mí (?)