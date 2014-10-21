# coding=utf-8
__author__ = 'gabriel'
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from twicles import defaults
from twicles.models import UserSettings

# Django datetime enconder
from django.core.serializers.json import DjangoJSONEncoder
from json import dumps

User = get_user_model()
from twicles.models import Twicle


def jsonify_twicle_queryset(twicles_queryset):
    """
    Takes a Twicle queryset and returns a JSON string
    :param twicles_queryset:    A Twicle queryset
    :return:                    A JSON string
    """
    twicles = []
    for twicle in twicles_queryset:
        twicles.append({
            'pk': twicle.id,
            'text': twicle.text,
            'author_username': twicle.author.username,
            'author_pk': twicle.author.id,
            'image': twicle.image.url if bool(twicle.image) else '',
            'created': twicle.created,
        })
    return twicles


def retrieve_subscribed_twicles(username, amount=defaults.twicles_per_page):
    """
    Retrieves the last <amount> of twicles published by
    the people <username> is following
    :param username:    twicles retrieved will belong to the people
                        that this <username> is following
                        (And depending on their settings, if they may also
                        have to be following <username>)
    :param amount:      the total amount of twicles that will be retrieved,
                        truncated depending on publication date
    :return:            a queryset of twicles ordered by publication date.
                        Newer first
    """
    if amount < defaults.twicles_per_page_min_value:
        raise ValueError('%s is less than the mimimum amount'
                         ' of twicles to retrieve' % amount)
    elif amount < 0:
        raise ValueError('%s is a negative amount'
                         'of twicles to retrieve' % amount)
    user = get_object_or_404(User, username=username)

    # QUESTION: Cómo mejorar estas querys?
    following_with_public_twicles = user.following.filter(
        id__in=UserSettings.objects.filter(
            visibility__exact=UserSettings.PUBLIC
        )
    )
    following_with_private_twicles_following_me = user.following.filter(
        id__in=UserSettings.objects.filter(
            visibility__exact=UserSettings.FOLLOWING
        )
    ).filter(
        id__in=user.followed_by.all()
    )
    # QUESTION
    # Joineo así?
    following_users = list(following_with_private_twicles_following_me) + list(following_with_public_twicles)

    # TODO: Agregar opciones de privacidad, que sólo obtenga los de aquellos que puede
    twicles = Twicle.objects.filter(author__in=following_users) \
                            .select_related('author') \
                            .order_by('-created')[:amount]

    return twicles


def retrieve_user_twicles(username,
                          amount=defaults.twicles_per_page,
                          requester=None):
    """
    Retrieves the last <amount> of twicles published by
    the user <username>
    :param username:    twicles retrieved will belong to <username>
    :param amount:      the total amount of twicles that will be retrieved,
                        truncated depending on publication date
    :param requester    user who is requesting the data. None if is anonymous
    :return:            a queryset of twicles that do NOT belong to <username>,
                        ordered by publication date. Newer first
    """
    if amount < defaults.twicles_per_page_min_value:
        raise ValueError('%s is less than the mimimum amount'
                         ' of twicles to retrieve' % amount)
    elif amount < 0:
        raise ValueError('%s is a negative amount'
                         'of twicles to retrieve' % amount)
    user = get_object_or_404(User, username=username)

    # QUESTION: Esto es un quilombo, pero es la mejor manera que encontré
    #   para hacerlo sin confundirme
    if user.usersettings.visibility == UserSettings.FOLLOWING:
        if not requester:
            twicles = Twicle.objects.none()
        else:
            if user.following.filter(id__in=requester.followed_by.all()).exists():
                twicles = Twicle.objects.filter(author__exact=user) \
                                        .order_by('-created')[:amount]
            else:
                twicles = Twicle.objects.none()
    else:
        twicles = Twicle.objects.filter(author__exact=user) \
                                .order_by('-created')[:amount]


    return twicles