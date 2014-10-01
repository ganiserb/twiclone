# coding=utf-8
__author__ = 'gabriel'

from django import forms
from twiclone.settings import AUTH_USER_MODEL
User = AUTH_USER_MODEL
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from users.models import User, InterestTag


class ProfileForm(forms.ModelForm):

    next = forms.CharField(widget=forms.HiddenInput())
    user_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ['avatar', 'bio', 'next', 'user_id']


class ProfileTagsForm(forms.ModelForm):

    next = forms.CharField(widget=forms.HiddenInput())
    user_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ['interest_tags', 'next', 'user_id']
        widgets = {
            'interest_tags': forms.CheckboxSelectMultiple(),
        }


class TagForm(forms.ModelForm):

    next = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = InterestTag
        fields = ['tag_name', 'next']


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'bio', 'avatar')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('password', 'bio', 'avatar')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]