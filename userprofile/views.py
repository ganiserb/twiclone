# coding=utf-8
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User
from userprofile.models import Profile
from userprofile.forms import ProfileForm


def show_profile(request, username):
    """
    Only shows the profile page of the given user
    """
    profile = get_object_or_404(Profile, user=get_object_or_404(User, username=username))

    form = ProfileForm(instance=profile)

    if request.method == 'POST' and profile.user == request.user:
        form = ProfileForm(request.POST)
    #else:

    return render(request, 'userprofile/show.html', {'profile': profile,
                                                     'interest_tags': profile.interest_tags.all(),
                                                     'show_edit_button': profile.user == request.user,
                                                     'form': form,
                                                     }
                  )


#TODO: Decorador para que sólo sea el propio
def edit_profile(request, username):
    """
    Allows the edition of the logged user profile
    """

    return render(request, 'userprofile/show.html')