# coding=utf-8
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core import serializers

from twicles import api


def home(request):
    twicles = serializers.serialize('json',
                                    api.retrieve_subscribed_twicles(request.user.username))
    return HttpResponse(twicles)

def profile(request, username):
    twicles = serializers.serialize('json',
                                    api.retrieve_user_twicles(username))
    return HttpResponse(twicles)