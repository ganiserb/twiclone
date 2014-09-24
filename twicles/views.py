# coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
User = get_user_model()

from twicles.models import Twicle
from twicles.forms import NewTwicleForm


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
                      'last_twicles': last_twicles,
                      'form_new_twicle': form_new_twicle,
                      'user_shown': user_shown,
                      'allow_editing': request.user == user_shown,
                  })


def post_twicle(request):
    """

    """

@login_required()
def follow(request, username):
    raise NotImplementedError