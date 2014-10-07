# coding=utf-8
__author__ = 'gabriel'
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from twicles import defaults

User = get_user_model()
from twicles.models import Twicle


def retrieve_subscribed_twicles(username, amount=defaults.twicles_per_page):
    """
    Retrieves the last <amount> of twicles published by
    the people <username> is following
    :param username:    twicles retrieved will belong to the people
                        that this <username> is following
    :param amount:      the total amount of twicles that will be retrieved,
                        truncated depending on publication date
    :return:            a queryset of twicles ordered by publication date.
                        Newer first
    """
    user = get_object_or_404(User, username=username)
    following_users = user.following.all()

    # TODO: Agregar opciones de privacidad, que sólo obtenga los de aquellos que puede
    twicles = Twicle.objects.filter(author__in=following_users) \
                            .order_by('-created')[:amount]

    return twicles


def retrieve_user_twicles(username, amount=defaults.twicles_per_page):
    """
    Retrieves the last <amount> of twicles published by
    the user <username>
    :param username:    twicles retrieved will belong to <username>
    :param amount:      the total amount of twicles that will be retrieved,
                        truncated depending on publication date
    :return:            a queryset of twicles that do NOT belong to <username>,
                        ordered by publication date. Newer first
    """
    user = get_object_or_404(User, username=username)
    twicles = Twicle.objects.filter(author__exact=user) \
                            .order_by('-created')[:amount]
    return twicles