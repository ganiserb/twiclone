# coding=utf-8
from django.shortcuts import \
    render,\
    get_object_or_404,\
    HttpResponseRedirect,\
    HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

from users.forms import ProfileForm, ProfileTagsForm, TagForm, UserCreationForm
from twicles.models import Twicle, UserSettings
from twicles.forms import NewTwicleForm


def register(request):
    """
    Shows and processes the registration form
    """
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


def show_profile(request, username):
    """
    Shows a user profile page including her twicle timeline
    If the user is authentcated also displays a form to post a twicle,
      starting with @username

    :param request:
    :param username: the User.username of the user whose profile wants to be
                        viewed
    """
    user_shown = get_object_or_404(User, username=username)
    if request.user.is_authenticated():
        amount = UserSettings.objects.get(user=request.user).twicles_per_page
        display_unfollow = request.user.following.filter(id=user_shown.id).exists()
    else:
        # TODO: No usar número mágico
        amount = 50  # QUESTION: Magic number - Ver la que está en users.models
        display_unfollow = None

    # QUESTION: Cómo hago estas líneas lindas y PEP8 a la vez? o_O
    twicles = Twicle.objects.filter(author=user_shown).order_by('-created')[:amount]

    new_twicle_form = NewTwicleForm(initial={
        'next': reverse(
            'users:show_profile',
            kwargs={'username': username}),
        'text': '@' + username + ' '})  # Start the twicle.text with @username

    return render(request,
                  'users/profile.html',
                  {'twicles': twicles,
                   'profile': user_shown,
                   'interest_tags': user_shown.interest_tags.all(),
                   'new_twicle_form': new_twicle_form,
                   'edition_allowed': False,
                   'following_count': user_shown.following.count(),
                   'followers_count': user_shown.followed_by.count(),
                   'display_unfollow': display_unfollow})


@login_required
def post_profile_form(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            # QUESTION: Cómo mejorar lo siguiente?
            # Extract the user from the hidden field
            user = get_object_or_404(User, id=profile_form.cleaned_data['user_id'])

            if request.user == user:
                # Recreate the form, but this time binded to the user instance
                profile_form = ProfileForm(request.POST, request.FILES, instance=user)
                profile_form.save()

                return HttpResponseRedirect(profile_form.cleaned_data['next'])
            else:
                raise PermissionDenied

        else:
            # Save the form in the session for the redirect
            request.session['profile_form_with_errors'] = request.POST.copy()
                # We're not saving the avatar image, though...

    # QUESTION: Si no viene un POST qué?
    return HttpResponseRedirect(request.POST['next'])


@login_required
def post_new_tag_form(request):
    if request.method == 'POST':
        new_tag_form = TagForm(request.POST)
        if new_tag_form.is_valid():
            new_tag_form.save()

            return HttpResponseRedirect(new_tag_form.cleaned_data['next'])
        else:
            request.session['new_tag_form_with_errors'] = request.POST

    return HttpResponseRedirect(request.POST['next'])



@login_required
def post_edit_tags_form(request):
    """
    Edits the tag cloud of the given user only if it belongs to him
    """
    if request.method == "POST":
        tags_form = ProfileTagsForm(request.POST)
        if tags_form.is_valid():
            user = get_object_or_404(User, id=tags_form.cleaned_data['user_id'])
            if request.user == user:
                # Only allow edition if the change afects the one
                #   who made the request
                tags_form = ProfileTagsForm(request.POST, instance=user)
                tags_form.save()

                return HttpResponseRedirect(tags_form.cleaned_data['next'])
            else:
                raise PermissionDenied
        else:
            request.session['edit_tags_form_with_errors'] = request.POST.copy()

    return HttpResponseRedirect(request.POST['next'])



@login_required
def post_edit_tags_form_JS(request):
    """
    Edits the tag cloud of the given user only if it belongs to him
    """
    if request.method == "POST":
        tags_form = ProfileTagsForm(request.POST)
        if tags_form.is_valid():
            user = get_object_or_404(User, id=tags_form.cleaned_data['user_id'])
            if request.user == user:
                # Only allow edition if the change afects the one
                #   who made the request
                tags_form = ProfileTagsForm(request.POST, instance=user)
                tags_form.save()

                # QUESTION: Este no tiene redirect porque sólo lo uso con JS.
                #   Qué hago? Es una cosa rara
                return HttpResponse("Actualización correcta")
            else:
                raise PermissionDenied

    return HttpResponse("Algo falló :/")


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

    return HttpResponseRedirect(reverse(
        'users:show_profile',
        kwargs={'username': username}))