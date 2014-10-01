# coding=utf-8
__author__ = 'gabriel'

from django.core.urlresolvers import reverse
from django import forms
from twicles.models import Twicle


class NewTwicleForm(forms.ModelForm):
    """
    Form for creating new Twicles
    """

    #action = reverse('twicles:post_twicle')   # QUESTION: Por qué no anda reverse acá? Lo estoy haciendo en la view a esto

    image = forms.ImageField(required=False)
    next = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Twicle
        fields = ['text', 'image', 'next']