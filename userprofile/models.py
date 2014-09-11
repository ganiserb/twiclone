from django.db import models
from django.contrib.auth.models import User

class InterestTag(models.Model):
    tag_name = models.CharField(max_length=25)

class Profile(User):
    avatar = models.ImageField(upload_to='user_avatars')
    interest_tags = models.ManyToManyField(InterestTag, related_name='users')