# coding=utf-8
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User
from userprofile.models import Profile


def show_profile(request, username):
    """
    Only shows the profile page of the given user
    """
    # u = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=get_object_or_404(User, username=username))
    #profile = Profile.objects.get(user=User.objects.get(username=username))
    return render(request, 'userprofile/show.html', {'profile': profile})


#TODO: Decorador para que sólo sea el propio
def edit_profile(request, username):
    return render(request, 'userprofile/edit.html')