# coding=utf-8
__author__ = 'gabriel'

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.urlresolvers import reverse
from twicles.models import Twicle, UserSettings


class NewTwicleForm(forms.ModelForm):
    """
    Form for creating new Twicles
    """

    next = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(NewTwicleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse('twicles:post_twicle')
        self.helper.add_input(Submit('submit', 'Publicar'))

    class Meta:
        model = Twicle
        fields = ['text', 'image', 'next']
        labels = {
            'text': 'Texto del twicle',
            'image': 'Incluir una imagen',
        }
        help_texts = {
            'image': 'Seleccionar una imagen guardada',
        }
        widgets = {
            'text': forms.Textarea()
        }


class UserSettingsForm(forms.ModelForm):
    """
    Form to edit the user Twicle settings
    """

    def __init__(self, *args, **kwargs):
        super(UserSettingsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse('twicles:post_user_settings')
        self.helper.add_input(Submit('submit', 'Guardar'))

    class Meta:
        model = UserSettings
        fields = ['visibility', 'twicles_per_page']
        labels = {
            'visibility': 'Visibilidad de tus twicles',
            'twicles_per_page': 'Twicles por página',
        }
        help_texts = {
            'visibility': 'Selecciona quién puede ver tus twicles',
            'twicles_per_page': 'Cuántos twicles quieres ver en la lista?',
        }
        widgets = {
            'visibility': forms.RadioSelect()
        }