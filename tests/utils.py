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


def get_response_with_authenticated_user(client, url, user=None):
    """
    If <user> is not provided it creates a test user, logs her in
    in the provided client and then returns the user instance
    and the response for the given url
    :param client:  A test Client to perform the operations
    :param url:     the url where the client sends the GET request
    :param user:    a user instance to log into the client
    :return:        (user_loged_in, get_response_to_url)
    """
    u = create_user('UsuarioCreadoParaHacerleLogin') if user is None else user
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