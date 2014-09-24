# coding=utf-8
__author__ = 'gabriel'

from django import forms
from twiclone.settings import AUTH_USER_MODEL
User = AUTH_USER_MODEL

from users.models import User, InterestTag


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['avatar', 'bio']


class ProfileTagsForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['interest_tags']
        widgets = {
            'interest_tags': forms.CheckboxSelectMultiple(),
        }


class TagForm(forms.ModelForm):

    class Meta:
        model = InterestTag
        fields = ['tag_name']