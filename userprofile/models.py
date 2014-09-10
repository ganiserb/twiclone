from django.db import models
from django.contrib.auth.models import User

class Profile(User):
    avatar = models.ImageField(upload_to='user_avatars')
    interest_tags = models.ManyToManyField(InterestTag, related_name='users')

class InterestTag(models.Model):
    tag_name = models.CharField(25)
