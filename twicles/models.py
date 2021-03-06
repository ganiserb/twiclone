# coding=utf-8
from django.db import models
from twiclone.settings import AUTH_USER_MODEL


class UserSettings(models.Model):
    """
    User specific settings about the content
    All of them must contain a default value (Except user! xD )
    """
    PUBLIC = 'PU'       # Everyone can see
    FOLLOWING = 'FI'    # Only those i'm following can see

    VISIBILITY_CHOICES = (
        (PUBLIC, 'Public'),
        (FOLLOWING, 'Those I follow'),
    )

    user = models.OneToOneField(AUTH_USER_MODEL, unique=True)
    visibility = models.CharField(max_length=2,
                                  choices=VISIBILITY_CHOICES,
                                  default=PUBLIC)

    twicles_per_page = models.PositiveSmallIntegerField(default=50)

    def __str__(self):
        return self.user.username


class Twicle(models.Model):
    """
    Represents a post by the user. May include a picture
    """
    text = models.CharField(max_length=200)
    author = models.ForeignKey(AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="twiclo_images", blank=True)

    def includes_image(self):
        """
        returns True if the twicle has an image or False if it's
        not present
        :return:    boolean
        """
        return bool(self.image)

    # Admin stuff QUESTION: Esto no queda mejor en admin.py? Estoy mezclando cosas
    #   del sitio de admin en el modelo así
    includes_image.boolean = True
    includes_image.short_description = "Includes image?"

    def __str__(self):
        return self.text
