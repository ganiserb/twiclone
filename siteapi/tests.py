# coding=utf-8
from django.test import TestCase
import unittest
from django.core.urlresolvers import reverse
from mock import patch, MagicMock
import json
from siteapi import views

from tests import utils

# JSON válido
# mocking de retrieve... que reciba bien los parámetros (con amount o sin)
# que si estoy logueado devuelva 200
# que si le tiro un post siga funcionando igual (?)

class CommonJsonViewTests(object):
    view = None
    url = None
    retrieve_function = None    # Function to mock for the views

    def test_authenticated_user_gets_http_200(self):
        user, rsp = utils.get_response_with_authenticated_user(self.client,
                                                               self.url)
        self.assertEquals(rsp.status_code, 200)

    def test_valid_json_resposne(self):
        user = utils.create_user('test')
        utils.create_twicles(user, 10)
        _, rsp = utils.get_response_with_authenticated_user(self.client,
                                                            self.url,
                                                            user=user)
        valid_json = True
        try:
            json.loads(rsp.content.decode('utf-8'))
        except ValueError:
            valid_json = False
        self.assertEquals(valid_json, True)

    # QUESTION: Cómo hago esto? Necesito pasar parametros por GET
    #   y ver que la función que mockeo que se usa adentro se llame bien
    #   O sea:
    #         si le paso parametros que se los pase a la funcion
    #         si no le paso nada, que use el por defecto
    #              (o sea, reciba 1 solo parámetro)

    # def test_retrieve_function_receives_amount_parameter_from_http_get(self):
    #     # Patch retrieve function with mock
    #     with patch(self.retrieve_function, new=MagicMock()) as rf:
    #         rsp = self.client.get(self.url + '?amount=a10')
    #         rf.assertCalledOnceWith(username='pepe', amount=10)


class HomeJsonViewTests(TestCase, CommonJsonViewTests):

    def view(self):
        self.view = views.home

    def setUp(self):
        self.retrieve_function = 'siteapi.views.api.retrieve_subscribed_twicles'
        self.view = views.home
        self.url = reverse('api:home')

    def test_anonymous_user_gets_http_403(self):
        rsp = self.client.get(self.url)
        self.assertEquals(rsp.status_code, 403)


class ProfileJsonView(TestCase, CommonJsonViewTests):

    def setUp(self):
        self.retrieve_function = 'siteapi.views.api.retrieve_user_twicles'
        self.view = views.home

        u = utils.create_user('pepe')   # User whose profile will be requested
        self.url = reverse('api:profile', kwargs={'username': u.username})

    def test_anonymous_user_gets_http_200(self):
        rsp = self.client.get(self.url)
        self.assertEquals(rsp.status_code, 200)

    def test_nonexistent_user_returns_404(self):
        rsp = self.client.get(reverse('api:profile',
                                      kwargs={'username': 'idonotexist'}))
        self.assertEquals(rsp.status_code, 404)