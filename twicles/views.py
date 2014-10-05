# coding=utf-8
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()
from twicles.models import UserSettings
from twicles.forms import NewTwicleForm
from users.forms import ProfileForm, ProfileTagsForm, TagForm

from twicles.api import retrieve_subscribed_twicles


@login_required
def post_twicle(request):
    """
    Captures the POST method of a NewTwicleForm
    """
    if request.method == 'POST':
        new_twicle_form = NewTwicleForm(request.POST, request.FILES)
        if new_twicle_form.is_valid():
            # Don't save yet, user binding pending
            twicle = new_twicle_form.save(commit=False)
            twicle.author = request.user
            twicle.save()
            return HttpResponseRedirect(new_twicle_form.cleaned_data['next'])
        else:
            request.session['new_twicle_form_with_errors'] = request.POST

    return HttpResponseRedirect(request.POST['next'])




@login_required
def home(request):
    amount = UserSettings.objects.get(user=request.user).twicles_per_page
    twicles = retrieve_subscribed_twicles(request.user, amount)

    if "profile_form_with_errors" in request.session:
        # Recover from session because it comes with errors
        profile_form = ProfileForm(request.session.get('profile_form_with_errors'))
        # Remove that key, otherwise it will use the form with errors again
        del request.session['profile_form_with_errors']
    else:
        profile_form = ProfileForm(instance=request.user,
                                   initial={'next': reverse('home'),
                                            'user_id': request.user.id})

    edit_tags_form = ProfileTagsForm(instance=request.user,
                                     initial={'next': reverse('home'),
                                              'user_id': request.user.id})

    if "new_tag_form_with_errors" in request.session:
        new_tag_form = TagForm(request.session.get('new_tag_form_with_errors'))
        del request.session['new_tag_form_with_errors']
    else:
        new_tag_form = TagForm(initial={'next': reverse('home')})

    # QUESTION: esta es la mejor manera de setear el 'next' de los forms
    # antes de mostrarlos? Acá en la view? Es el lugar más lógico porque
    # yo se que el usuario tiene que volver acá. En un template no porque puedo
    # usar ese form desde otra view...
    if "new_twicle_form_with_errors" in request.session:
        new_twicle_form = NewTwicleForm(request.session.get('new_twicle_form_with_errors'))
        del request.session['new_twicle_form_with_errors']
    else:
        new_twicle_form = NewTwicleForm(initial={'next': reverse('home')})


    return render(request,
                  'twicles/home.html',
                  {'twicles': twicles,
                   'profile': request.user,
                   'edition_allowed': True,  # Si ve la home es porque es su propio perfil
                   'profile_form': profile_form,
                   'new_tag_form': new_tag_form,
                   'edit_tags_form': edit_tags_form,
                   'following_count': request.user.following.count(),
                   'followers_count': request.user.followed_by.count(),
                   'new_twicle_form': new_twicle_form,
                   'cosa': b"\u00a0"})   # TODO: Quitar! (Y de base.html tambien)