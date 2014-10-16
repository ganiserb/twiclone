# coding=utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponse
from mock import patch, MagicMock
import json
from siteapi import views

from tests import utils


class CommonJsonViewTests(object):
    view = None
    url = None
    retrieve_function = None    # Function to mock for the views
    # Common for all JSON views
    jsonify_function = 'siteapi.views.api.jsonify_twicle_queryset'

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
        self.assertEquals(rsp['Content-Type'], 'application/json')

    def test_retrieve_function_receives_amount_parameter_from_http_get(self):
        # Patch retrieve function with mock
        with patch(self.retrieve_function, new=MagicMock()) as rf:
            rsp = self.client.get(self.url + '?amount=10')
            rf.assertCalledOnceWith(username='pepe', amount=10)

    def test_view_obtains_twicles_from_retrieve_function(self):
        retrieve_function_mock = MagicMock()
        jsonify_function_mock = MagicMock()
        json_response_mock = MagicMock()

        retrieve_function_mock.return_value = ['test']
        jsonify_function_mock.return_value = 'blah, this is json'

        json_response_mock.return_value = HttpResponse()

        with patch(self.retrieve_function, new=retrieve_function_mock), \
             patch(self.jsonify_function, new=jsonify_function_mock), \
             patch('siteapi.views.JsonResponse', new=json_response_mock):
            # With these two functions patched, we can now call the view
            #   (but authenticated, so it works for both views)

            user, rsp = utils.get_response_with_authenticated_user(
                self.client,
                self.url
            )

            self.assertTrue(retrieve_function_mock.called)
            self.assertEquals(retrieve_function_mock.call_count, 1)

            self.assertTrue(jsonify_function_mock.called)
            self.assertEquals(jsonify_function_mock.call_count, 1)


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