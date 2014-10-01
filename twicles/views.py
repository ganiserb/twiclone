# coding=utf-8
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()
from twicles.models import Twicle, UserSettings
from twicles.forms import NewTwicleForm
from users.forms import ProfileForm, ProfileTagsForm, TagForm

from twicles.api import retrieve_subscribed_twicles


def view_twicles(request, username):    # TODO: Manejar el post del twicle en otra view
    """
    Shows the last twicles of the given user
    If this is the request.user page, allows for publication of new twicles
    """
    user_shown = get_object_or_404(User, username=username)

    if request.method == 'POST' and request.user == user_shown:
        form_new_twicle = NewTwicleForm(request.POST, request.FILES)
        if form_new_twicle.is_valid():
            twicle = form_new_twicle.save(commit=False)  # Don't save yet, pending actions

            twicle.author = request.user

            twicle.save()   # Done!

    # Always create a new form so it's ready to be used (Enven after processing a POST)
    form_new_twicle = NewTwicleForm()

    # TODO: Tomar la cantidad a mostrar de las settings del request.user
    last_twicles = Twicle.objects.filter(author=user_shown).order_by('-created')[:3]

    return render(request,
                  'twicles/view.html',
                  {
                      'twicles': last_twicles,
                      'form_new_twicle': form_new_twicle,
                      'user_shown': user_shown,
                      'allow_editing': request.user == user_shown,
                      'display_unfollow': request.user.following.filter(id=user_shown.id).exists(),
                  })


def post_twicle(request):   # QUESTION: Cómo muestro los errores del form así? Tendría que tener una vista sólo para eso?
    """
    Captures the POST method of a NewTwicleForm
    """
    if request.method == 'POST':
        new_twicle_form = NewTwicleForm(request.POST, request.FILES)
        if new_twicle_form.is_valid():
            twicle = new_twicle_form.save(commit=False)  # Don't save yet, user binding pending
            twicle.author = request.user
            twicle.save()

        return HttpResponseRedirect(new_twicle_form.cleaned_data['next'])


@login_required
def home(request):
    amount = UserSettings.objects.get(user=request.user).twicles_per_page
    twicles = retrieve_subscribed_twicles(request.user, amount)

    # Create the forms for the template
    profile_form = ProfileForm(instance=request.user,
                               initial={'next': reverse('home'),
                                        'user_id': request.user.id})

    edit_tags_form = ProfileTagsForm(instance=request.user,
                                     initial={'next': reverse('home'),
                                              'user_id': request.user.id})
    #TODO: edit_tags_form.action = reverse('users:')

    new_tag_form = TagForm(initial={'next': reverse('home')})
    #TODO: new_tag_form.action = reverse('twicles:post_twicle')

    # QUESTION: esta es la mejor manera de setear el 'next' de los forms? Tengo que usar ese metodo
    # de request porque sino el HTTPRedirect me tira a cualquier lado
    new_twicle_form = NewTwicleForm(initial={'next': reverse('home')})
    new_twicle_form.action = reverse('twicles:post_twicle')

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
                   'new_twicle_form': new_twicle_form})