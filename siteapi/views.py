# coding=utf-8
from django.shortcuts import HttpResponse
from django.http import HttpResponseForbidden

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

    if request.user.is_authenticated():
        # Build a parameters tuple to call the api function later
        param = (request.user.username,)
        if 'amount' in request.GET:
            # There's an "amount" of twicles in the request,
            #   so we add it to the parameters
            amount = int(request.GET['amount'])  # Puede reventar
            param += (amount,)

        twicles = api.jsonify_twicle_queryset(
            api.retrieve_subscribed_twicles(*param)
        )

        return HttpResponse(twicles)
    else:
        return HttpResponseForbidden("User not logged in")


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