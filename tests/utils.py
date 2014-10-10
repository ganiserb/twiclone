# coding=utf-8
__author__ = 'gabriel'

from twicles.models import Twicle
from django.contrib.auth import get_user_model
User = get_user_model()


def create_user(username):
    """
    Creates a new user that has matching username and password
    :param username:
    :return:
    """
    # Set the user up
    u = User.objects.create(username=username)
    u.set_password(username)
    u.save()
    return u


def get_response_with_authenticated_user(client, url):
    """
    Creates a test user, logs her in in the provided client,
    then returns the user instance and the response to the given url
    :param client:  A test Client to perform the operations
    :param url:     the url where the client sends the GET request
    :return:        (user_loged_in, get_response_to_url)
    """
    u = create_user('UsuarioCreadoParaHacerleLogin')
    # Log the user in
    client.login(username=u.username, password=u.username)
    # Get the home page
    return u, client.get(url)


def create_twicles(user, amount):
    """
    Creates a number of <amount> twicles asociated to the <user>
    :param user:    The author for the twicles
    :param amount:  The amount to create
    :return:        List of twicles created
    """
    # QUESTION: Cómo hacer esto PEP8?
    return [Twicle.objects.create(text='twicle' + str(n)
                                       + str(user.username),
                                  author=user)
            for n in range(amount)]