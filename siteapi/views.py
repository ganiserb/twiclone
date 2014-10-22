# coding=utf-8
from django.http import HttpResponseForbidden, JsonResponse, Http404

from twicles import api


def home(request):
    """
    Returns an HTTPRequest with a JSON string containing all the Twicles
    that should be displayed in the home timeline of the request.user
    Results come from api.retrieve_subscribed_twicles
    :param request:
    :return:
    """
    if request.user.is_authenticated():
        # Build parameters to call the api function later
        kwargs = {'username': request.user.username}

        if 'amount' in request.GET:
            # There's an "amount" of twicles in the request,
            #   so we add it to the parameters
            try:    # QUESTION: Está bien hacer esto? Si no puede convertit a int porque me ponen un string, dejo que reviente?
                kwargs['amount'] = int(request.GET['amount'])
            except ValueError:
                raise Http404

        twicles = api.jsonify_twicle_queryset(
            api.retrieve_subscribed_twicles(**kwargs)
        )

        return JsonResponse(twicles, safe=False)
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
    kwargs = {'username': username,
              'requester': request.user}
    if 'amount' in request.GET:
        try:    # QUESTION: Está bien hacer esto? Si no puede convertit a int porque me ponen un string, dejo que reviente?
            kwargs['amount'] = int(request.GET['amount'])
        except ValueError:
            raise Http404

    twicles = api.jsonify_twicle_queryset(
        api.retrieve_user_twicles(**kwargs)
    )

    return JsonResponse(twicles, safe=False)