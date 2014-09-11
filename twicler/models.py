from django.db import models
from django.contrib.auth.models import User

class Twiclo(models.Model):
    text = models.CharField(max_length=200)
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)


class UserSettings(User):   # TODO: User?
    PUBLIC = 'PU'       # Everyone can see
    FOLLOWING = 'FI'    # Only those i'm following can see

    VISIBILITY_CHOICES = (
        (PUBLIC, 'Public'),
        (FOLLOWING, 'Those I follow'),
    )

    visibility = models.CharField(max_length=2,
                                  choices=VISIBILITY_CHOICES,
                                  default=PUBLIC)
    following = models.ManyToManyField('self')
    followers = models.ManyToManyField('self')