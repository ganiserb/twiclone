# coding=utf-8
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

from users.forms import ProfileForm, ProfileTagsForm, TagForm, UserCreationForm


def register(request):
    if request.method == 'POST':
        registration_form = UserCreationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        registration_form = UserCreationForm()

    return render(request,
                  'users/register.html',
                  {'registration_form': registration_form})

#
# def show_profile(request, username):
#     """
#     Shows the profile page of the given username
#     If the profile belongs to the current user this view provides forms for:
#         Editing basic profile info
#         Selecting interest tags
#         Adding new interest tags
#     """
#
#     # TODO: REHACER TODO!
#     form_info = None
#     form_tags = None
#     form_new_tag = None
#
#     user_profile = get_object_or_404(User, username=username)
#
#     if user_profile == request.user:
#         form_info = ProfileForm(instance=user_profile)
#         form_tags = ProfileTagsForm(instance=user_profile)   # Este no se va a manejar en esta view, sino por AJAX
#         form_new_tag = TagForm()    # La idea es sólo crear nuevos tags
#
#     if request.method == 'POST' and user_profile == request.user:
#         if "form_info" in request.POST:
#             form_info = ProfileForm(request.POST, request.FILES, instance=user_profile)
#             if form_info.is_valid():
#                 form_info.save()
#
#         elif "form_new_tag" in request.POST:
#             form_new_tag = TagForm(request.POST)
#             if form_new_tag.is_valid():
#                 new_tag = form_new_tag.save()
#
#                 user_profile.interest_tags.add(new_tag)  # Add the the tag as a if the user chose it
#
#     return render(request,
#                   'users/profile.html',
#                   {'profile': user_profile,
#                    'interest_tags': user_profile.interest_tags.all(),
#                    'edition_allowed': request.user == user_profile,
#                    'form_info': form_info,
#                    'form_tags': form_tags,
#                    'form_new_tag': form_new_tag,
#                    'following_count': user_profile.following.count(),
#                    'followers_count': user_profile.followed_by.count(),
#                    'display_unfollow': request.user.following.filter(id=user_profile.id).exists()})


def post_profile_form(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            # QUESTION: Cómo mejorar lo siguiente?
            # Extract the user from the hidden field
            user = get_object_or_404(User, id=profile_form.cleaned_data['user_id'])
            # Recreate the form, but this time binded to the user instance
            profile_form = ProfileForm(request.POST, request.FILES, instance=user)

            profile_form.save()

            return HttpResponseRedirect(profile_form.cleaned_data['next'])

    #!!!!!!!! TODO: no tiene otro return esto


def post_new_tag_form(request):
    if request.method == 'POST':
        new_tag_form = TagForm(request.POST)

        if new_tag_form.is_valid():
            new_tag_form.save()

            return HttpResponseRedirect(new_tag_form.cleaned_data['next'])


# TODO: Que sólo pueda editar si es el mismo que la request
def post_edit_tags_form(request):
    """
    Edits the tag cloud of the given user only if it belongs to him
    """
    if request.method == "POST":
        tags_form = ProfileTagsForm(request.POST)
        if tags_form.is_valid():
            user = get_object_or_404(User, id=tags_form.cleaned_data['user_id'])
            tags_form = ProfileTagsForm(request.POST, instance=user)

            tags_form.save()

            # QUESTION: Este no tiene redirect porque sólo lo uso con JS. Qué hago?
            return HttpResponse("Actualización correcta")

    return HttpResponse("Algo falló :/")    # TODO: Que JS se encargue de decirle al usuario qué falló si hubo algo


@login_required
def follow_control(request, username, action):
    """
    Adds or removes the requested user to the <following> list of the currently logged in user
    """
    requested_user = get_object_or_404(User, username=username)
    exists = request.user.following.filter(id=requested_user.id).exists()

    # QUESTION: Esto está funcionando con GET. Para hacerlo con POST, pero
    #   sin andar usando un form (Es realmente necesario?) cómo hago?
    #   O sea, sin tener un <form> hardcodeado en el template, ni una clase Form
    #   ni con JS... Hay alguna manera de que sea sencillo como con el GET?
    if exists and action == 'u':
        request.user.following.remove(requested_user)

    if not exists and action == 'f':
        request.user.following.add(requested_user)

    return HttpResponseRedirect(reverse('twicles:view', kwargs={'username': username}))