# coding=utf-8
__author__ = 'gabriel'

from django import forms
from userprofile.models import Profile, InterestTag


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class ProfileTagsForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['interest_tags']
        widgets = {
            'interest_tags': forms.CheckboxSelectMultiple(),
        }


class TagForm(forms.ModelForm):

    class Meta:
        model = InterestTag
        fields = ['tag_name']