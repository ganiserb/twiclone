# coding=utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse

from twicles.forms import NewTwicleForm
from tests import utils
from django.contrib.auth import get_user_model
User = get_user_model()


class ShowProfileViewTests(TestCase):

    def test_status_code_always_200(self):
        u = utils.create_user('usuario')
        rsp = self.client.get(reverse('users:show_profile',
                                      kwargs={'username': u.username}))
        self.assertEquals(rsp.status_code, 200)

    def test_correct_context_variables_passed_to_template(self):
        user, rsp = utils.get_response_with_authenticated_user(self.client,
                                                               reverse('home'))
        # profile context variable should be
        #   the user object that made the request
        self.assertEquals(rsp.context['profile'], user)
        self.assertIn('twicles', rsp.context.keys())
        self.assertIsInstance(rsp.context['followers_count'], int)
        self.assertIsInstance(rsp.context['following_count'], int)
        self.assertIsInstance(rsp.context['new_twicle_form'], NewTwicleForm)