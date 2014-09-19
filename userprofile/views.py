# coding=utf-8
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from userprofile.models import Profile
from userprofile.forms import ProfileForm, ProfileTagsForm


def view_profile(request, username):
    """
    Only shows the profile page of the given user
    """
    form_info = None
    form_tags = None
    edition_allowed = False

    profile = get_object_or_404(Profile, user=get_object_or_404(User, username=username))

    if profile.user == request.user:
        form_info = ProfileForm(instance=profile)

        form_tags = ProfileTagsForm(instance=profile)   # Este no se va a manejar en esta view, sino por AJAX

        edition_allowed = True

    if request.method == 'POST' and profile.user == request.user:
        form_info = ProfileForm(request.POST, request.FILES, instance=profile)   # TODO: Funcionaría la img con ajax?
        if form_info.is_valid():
            form_info.save()

            return HttpResponseRedirect(reverse('userprofile:view', kwargs={'username': username}))
    else:

        return render(request, 'userprofile/show.html', {'profile': profile,
                                                         'interest_tags': profile.interest_tags.all(),
                                                         'edition_allowed': edition_allowed,
                                                         'form_info': form_info,
                                                         'form_tags': form_tags,
                                                         }
                      )


#TODO: Decorador para que sólo sea el propio
def edit_tags_ajax(request, username):
    """
    Edits the tag cloud of the given user only if it belongs to him. The request comes from a JS event
    """

    profile = get_object_or_404(Profile, user=get_object_or_404(User, username=username))

    if request.method == "POST" and profile.user == request.user:
        tags_form = ProfileTagsForm(request.POST, instance=profile)
        if tags_form.is_valid():
            tags_form.save()

            return HttpResponse("Actualización correcta: " + username)

    return HttpResponse("Algo falló :/")    # TODO: Qué hacer en este caso? Levantar un error 500?