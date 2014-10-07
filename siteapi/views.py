# coding=utf-8
from django.shortcuts import HttpResponse

from twicles import api


def home(request):
    """
    Returns an HTTPRequest with a JSON string containing all the Twicles
    that should be displayed in the home timeline of the request.user
    Results come from api.retrieve_subscribed_twicles
    :param request:
    :return:
    """
    # QUESTION: Esto es muy ilegible? Setear este parametro opcional así?
    param = (request.user.username,)
    if 'amount' in request.GET:
        amount = int(request.GET['amount'])  # Puede reventar
        param += (amount,)

    twicles = api.jsonify_twicle_queryset(
        api.retrieve_subscribed_twicles(*param)
    )

    return HttpResponse(twicles)


def profile(request, username):
    """
    Returns an HTTPRequest with a JSON string containing all the Twicles
    that <username> published. Results come form api.retrieve_user_twicles
    The amount can be controled by the GET parameter "amount"
    :param request:
    :param username:    The <username> of the user whose Twicles are requested
    :return:
    """
    param = (username,)
    if 'amount' in request.GET:
        amount = int(request.GET['amount'])  # Puede reventar
        param += (amount,)

    twicles = api.jsonify_twicle_queryset(
        api.retrieve_user_twicles(*param)
    )

    return HttpResponse(twicles)