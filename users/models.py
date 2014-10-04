# coding=utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser
#from twiclone import settings
# QUESTION: Cómo tener en settings la constante del avatar o la cantidad de posts a mostrar en twicle.UserSettings?
# O sea, definir acá algo así:
# settings.USERS_DEFAULT_AVATAR if settings.USERS_DEFAULT_AVATAR else 'default.jpg'
# La idea es que esta app ya tenga una por defecto y se pueda sobreescribir
#   en el settings.py
# http://stackoverflow.com/questions/8428556/django-default-settings-convention-for-pluggable-app


class InterestTag(models.Model):
    tag_name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.tag_name


class User(AbstractUser):
    """
    This extends the built-in user model with profile info
    """
    avatar = models.ImageField(upload_to='user_avatars',
                               default="default.jpg")
    bio = models.CharField(max_length=200)
    interest_tags = models.ManyToManyField(InterestTag,
                                           related_name='users_interested',
                                           blank=True)
    following = models.ManyToManyField("self",
                                       symmetrical=False,
                                       related_name="followed_by",
                                       blank=True)

    def save(self, *args, **kwargs):
        # Follow myself
        super(User, self).save(*args, **kwargs)
        if not self.following.filter(id=self.id).exists():
            self.following.add(self)
