# coding=utf-8
__author__ = 'gabriel'

from django import forms
from twicler.models import Twiclo


class NewTwicleForm(forms.ModelForm):

    image = forms.ImageField(required=False)

    class Meta:
        model = Twiclo
        fields = ['text', 'image']