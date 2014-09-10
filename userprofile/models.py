from django.db import models

class Profile(models.Model):
    avatar = models.ImageField(upload_to='user_avatars')

class InteresTag(models.Model):
    tag_name = models.CharField(25)
