# coding=utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponse
from mock import patch, MagicMock, call
import json
from siteapi import views

from tests import utils


class CommonJsonViewTests(object):
    """
    Tests that should pass all JSON views
    For each view TestCase the following
    attributes must be defined on SetUp:

    view        the view function itself
    url         the url the client uses to access the view
                (do a reverse)
    retrieve_function   a string containing the path to the
                        retrieve function, to be able to patch it
    """
    url = None
    retrieve_function = None    # Function to mock for the views
    # Common for all JSON views
    jsonify_function = 'siteapi.views.api.jsonify_twicle_queryset'

    def test_authenticated_user_gets_http_200(self):
        """Tests if an authenticated user can access the JSON api views"""
        user, rsp = utils.get_response_with_authenticated_user(self.client,
                                                               self.url)
        self.assertEquals(rsp.status_code, 200)

    def test_valid_json_resposne(self):
        """
        All JSON views should return valid JSON text and
        include the JSON Content-Type header
        """
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
        """
        JSON views that return a list of things must capture
        the <amount> parameter of the GET method and use it to
        return that amount of things
        """
        # Patch retrieve function with mock
        with patch(self.retrieve_function, new=MagicMock()) as rf:
            self.client.get(self.url + '?amount=10')
            rf.assertCalledOnceWith(username='pepe', amount=10)

    def test_view_obtains_twicles_from_retrieve_function(self):
        """
        Checks that the api functions are actually called
        to get the twicles
        """
        retrieve_function_mock = MagicMock()
        jsonify_function_mock = MagicMock()
        json_response_mock = MagicMock()

        retrieve_function_mock.return_value = ['test']
        jsonify_function_mock.return_value = 'blah, this is json'

        json_response_mock.return_value = HttpResponse()

        with patch(self.retrieve_function, new=retrieve_function_mock),\
            patch(self.jsonify_function, new=jsonify_function_mock),\
            patch('siteapi.views.JsonResponse', new=json_response_mock):

            # With these two functions patched, we can now call the view
            #   (but authenticated, so it works for both views)

            utils.get_response_with_authenticated_user(
                self.client,
                self.url
            )

            self.assertTrue(retrieve_function_mock.called)
            self.assertEquals(retrieve_function_mock.call_count, 1)

            self.assertTrue(jsonify_function_mock.called)
            self.assertEquals(jsonify_function_mock.call_count, 1)


class HomeJsonViewTests(TestCase, CommonJsonViewTests):

    def setUp(self):
        self.retrieve_function = 'siteapi.views.api.retrieve_subscribed_twicles'
        self.view = views.home
        self.url = reverse('api:home')

    def test_anonymous_user_gets_http_403(self):
        rsp = self.client.get(self.url)
        self.assertEquals(rsp.status_code, 403)

    def test_view_calls_api_function_correctly(self):
        # QUESTION: Se repite prácticamente todo para la otra view... :/
        request = MagicMock()
        request.user.is_authenticated.return_value = True
        request.user.username = 'test'
        request.GET = {}

        function_mock = MagicMock()

        with patch('siteapi.views.api.retrieve_subscribed_twicles',
                   new=function_mock),\
            patch('siteapi.views.api.jsonify_twicle_queryset',
                  new=MagicMock()),\
            patch('siteapi.views.JsonResponse',
                  new=MagicMock()):

            self.view(request)

            request.GET['amount'] = '111'
            self.view(request)

            function_mock.assert_has_calls(
                [call(username=request.user.username),
                 call(username=request.user.username, amount=111)]
            )


class ProfileJsonView(TestCase, CommonJsonViewTests):

    def setUp(self):
        self.retrieve_function = 'siteapi.views.api.retrieve_user_twicles'
        self.view = views.profile

        u = utils.create_user('pepe')   # User whose profile will be requested
        self.url = reverse('api:profile', kwargs={'username': u.username})

    def test_anonymous_user_gets_http_200(self):
        rsp = self.client.get(self.url)
        self.assertEquals(rsp.status_code, 200)

    def test_nonexistent_user_returns_404(self):
        rsp = self.client.get(reverse('api:profile',
                                      kwargs={'username': 'idonotexist'}))
        self.assertEquals(rsp.status_code, 404)

    def test_view_calls_api_function_correctly(self):
        # QUESTION: Se repite prácticamente todo para la otra view... :/
        request = MagicMock()
        request.user.is_authenticated.return_value = True
        request.user.username = 'test'
        request.GET = {}

        function_mock = MagicMock()

        with patch('siteapi.views.api.retrieve_user_twicles',
                   new=function_mock),\
            patch('siteapi.views.api.jsonify_twicle_queryset',
                  new=MagicMock()),\
            patch('siteapi.views.JsonResponse',
                  new=MagicMock()):

            self.view(request, 'pepe')

            request.GET['amount'] = '111'
            self.view(request, 'pepe')

            function_mock.assert_has_calls(
                [call(username='pepe', requester=request.user),
                 call(username='pepe', amount=111, requester=request.user)]
            )