# coding=utf-8
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from users.models import User
from userprofile.forms import ProfileForm, ProfileTagsForm, TagForm


def view_profile(request, username):
    """
    Shows the profile page of the given user
    If the profile belongs to the current user allows:
        Edit basic profile info
        Select interest tags
        Add new interest tags
    """

    # TODO: REHACER TODO!
    form_info = None
    form_tags = None
    form_new_tag = None
    edition_allowed = False

    user_profile = get_object_or_404(User, username)

    if user_profile.user == request.user:
        form_info = ProfileForm(instance=user_profile)

        form_tags = ProfileTagsForm(instance=user_profile)   # Este no se va a manejar en esta view, sino por AJAX

        form_new_tag = TagForm()    # La idea es sólo crear nuevos

        edition_allowed = True

    if request.method == 'POST' and user_profile.user == request.user:
        if "form_info" in request.POST:
            form_info = ProfileForm(request.POST, request.FILES, instance=user_profile)   # TODO: Funcionaría la img con ajax? -> En teoría sí
            if form_info.is_valid():
                form_info.save()

        elif "form_new_tag" in request.POST:
            form_new_tag = TagForm(request.POST)
            if form_new_tag.is_valid():
                new_tag = form_new_tag.save()

                user_profile.interest_tags.add(new_tag)  # Add the the tag as a if the user chose it

        return HttpResponseRedirect(reverse('userprofile:view', kwargs={'username': username}))

    else:

        return render(request, 'userprofile/show.html', {'profile': user_profile,
                                                         'interest_tags': user_profile.interest_tags.all(),
                                                         'edition_allowed': edition_allowed,
                                                         'form_info': form_info,
                                                         'form_tags': form_tags,
                                                         'form_new_tag': form_new_tag,
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

    return HttpResponse("Algo falló :/")    # TODO: Que JS se encargue de decirle al usuario qué falló si hubo algo