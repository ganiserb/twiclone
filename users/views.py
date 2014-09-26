# coding=utf-8
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

from users.forms import ProfileForm, ProfileTagsForm, TagForm


def show_profile(request, username):
    """
    Shows the profile page of the given username
    If the profile belongs to the current user this view provides forms for:
        Editing basic profile info
        Selecting interest tags
        Adding new interest tags
    """

    # TODO: REHACER TODO!
    form_info = None
    form_tags = None
    form_new_tag = None

    user_profile = get_object_or_404(User, username=username)

    if user_profile == request.user:
        form_info = ProfileForm(instance=user_profile)
        form_tags = ProfileTagsForm(instance=user_profile)   # Este no se va a manejar en esta view, sino por AJAX
        form_new_tag = TagForm()    # La idea es sólo crear nuevos tags

    if request.method == 'POST' and user_profile == request.user:
        if "form_info" in request.POST:
            form_info = ProfileForm(request.POST, request.FILES, instance=user_profile)
            if form_info.is_valid():
                form_info.save()

        elif "form_new_tag" in request.POST:
            form_new_tag = TagForm(request.POST)
            if form_new_tag.is_valid():
                new_tag = form_new_tag.save()

                user_profile.interest_tags.add(new_tag)  # Add the the tag as a if the user chose it

        return HttpResponseRedirect(reverse('users:show_profile', kwargs={'username': username}))

    else:

        return render(request,
                      'users/show.html',
                      {'profile': user_profile,
                       'interest_tags': user_profile.interest_tags.all(),
                       'edition_allowed': request.user == user_profile,
                       'form_info': form_info,
                       'form_tags': form_tags,
                       'form_new_tag': form_new_tag,
                       'following_count': user_profile.following.count(),
                       'followers_count': user_profile.followed_by.count(),
                       # QUESTION: Qué tal es la sig consulta? La recomienda la docu: https://docs.djangoproject.com/en/1.7/ref/models/querysets/#exists
                       # Me refiero al id=u_p.id... Está bien usar id? Parece "burda" la manera de hacerlo
                       'display_unfollow': request.user.following.filter(id=user_profile.id).exists(),
                       }
        )


def post_profile_info(request, username):   # QUESTION: Conviene tener el username en la url o en un hidden field del form?
    user_profile = get_object_or_404(User, username=username)

    if request.method == 'POST' and request.user == user_profile:
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
        else:
            return render(request,
                          'users/show.html',
                          {'profile': user_profile,
                           'interest_tags': user_profile.interest_tags.all(),
                           'edition_allowed': request.user == user_profile,
                           'form_info': form,
                           }
                          )

    return HttpResponseRedirect(reverse('users:view', kwargs={'username': username}))


# TODO: Decorador para que sólo sea el propio
def edit_tags_ajax(request, username):
    """
    Edits the tag cloud of the given user only if it belongs to him. The request comes from a JS event
    """
    user_profile = User.objects.get(username=username)
    #user_profile = get_object_or_404(User, username=username)

    if request.method == "POST" and user_profile == request.user:
        tags_form = ProfileTagsForm(request.POST, instance=user_profile)
        if tags_form.is_valid():
            tags_form.save()

            return HttpResponse("Actualización correcta: " + username)

    return HttpResponse("Algo falló :/")    # TODO: Que JS se encargue de decirle al usuario qué falló si hubo algo


@login_required
def follow_control(request, username):
    """
    Adds or removes the requested user to the <following> list of the currently logged in user
    """
    requested_user = get_object_or_404(User, username=username)
    exists = request.user.following.filter(id=requested_user.id).exists()

    # QUESTION: Hacer follow / unfollow en la misma vista era más fácil. Cómo lo hubieras hecho?
    if exists:
        request.user.following.remove(requested_user)
    else:
        request.user.following.add(requested_user)

    return HttpResponseRedirect(reverse('users:show_profile', kwargs={'username': username}))