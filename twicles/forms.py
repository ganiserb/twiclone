# coding=utf-8
__author__ = 'gabriel'

from django import forms
from twicles.models import Twicle


class NewTwicleForm(forms.ModelForm):

    image = forms.ImageField(required=False)

    class Meta:
        model = Twicle
        fields = ['text', 'image']