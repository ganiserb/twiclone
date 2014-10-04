# coding=utf-8
__author__ = 'gabriel'

from django.core.urlresolvers import reverse
from django import forms
from twicles.models import Twicle


class NewTwicleForm(forms.ModelForm):
    """
    Form for creating new Twicles
    """

    image = forms.ImageField(required=False)
    next = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Twicle
        fields = ['text', 'image', 'next']