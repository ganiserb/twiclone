# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


class InterestTag(models.Model):
    tag_name = models.CharField(max_length=25)


class Profile(models.Model):
    """
    The user profile model that extends the user model with a OneToOne link
    """
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='user_avatars')
    interest_tags = models.ManyToManyField(InterestTag, related_name='users')