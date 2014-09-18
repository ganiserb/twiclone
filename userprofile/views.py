# coding=utf-8
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from userprofile.models import Profile
from userprofile.forms import ProfileForm


def view_profile(request, username):
    """
    Only shows the profile page of the given user
    """
    form = None
    edition_allowed = False

    profile = get_object_or_404(Profile, user=get_object_or_404(User, username=username))

    if profile.user == request.user:
        form = ProfileForm(instance=profile)
        edition_allowed = True

    if request.method == 'POST' and profile.user == request.user:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('userprofile:view', kwargs={'username': username}))
    else:

        return render(request, 'userprofile/show.html', {'profile': profile,
                                                         'interest_tags': profile.interest_tags.all(),
                                                         'edition_allowed': edition_allowed,
                                                         'form': form,
                                                         }
                      )


#TODO: Decorador para que sólo sea el propio
def edit_profile(request, username):
    """
    Allows the edition of the logged user profile
    """

    return render(request, 'userprofile/show.html')