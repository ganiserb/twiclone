# coding=utf-8
__author__ = 'gabriel'

from django import forms
from userprofile.models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']