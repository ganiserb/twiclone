# coding=utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse

from twicles.api import retrieve_subscribed_twicles
from twicles.models import Twicle
from twicles import defaults, forms
import users
from django.contrib.auth import get_user_model
User = get_user_model()


class ApiRetrieveSubscribedTwiclesTests(TestCase):

    def create_twicles(self, user, amount):
        """
        Creates a number of <amount> twicles asociated to the <user>
        :param user:    The author for thetwicles
        :param amount:  The amount to create
        :return:        List of twicles created
        """
        # QUESTION: Cómo hacer esto PEP8?
        return [Twicle.objects.create(text='twicle' + str(n)
                                           + str(user.username),
                                      author=user)
                for n in range(amount)]

    def test_amount_parameter_raises_value_error_if_amount_less_than_minimum(self):
        """
        tests that the api function raises a value error when the
        amount parameter is less than the minimum defined by default
        """
        u1 = User.objects.create(username='u1')
        self.assertRaises(ValueError,
                          retrieve_subscribed_twicles,
                          username=u1.username,
                          amount=defaults.twicles_per_page_min_value - 1)

    def test_amount_parameter_raises_value_error_if_amount_negative(self):
        """
        tests that the api function raises a value error when the
        amount parameter is negative
        """
        u1 = User.objects.create(username='u1')
        self.assertRaises(ValueError,
                          retrieve_subscribed_twicles,
                          username=u1.username,
                          amount=-defaults.twicles_per_page_min_value)

    def test_user_without_twicles_or_following_returns_empty_queryset(self):
        u1 = User.objects.create(username='u1')
        self.assertQuerysetEqual(retrieve_subscribed_twicles(u1.username),
                                 User.objects.none())  # Compare to empty QS

    def test_returns_as_many_twicles_as_amount_or_less(self):
        u1 = User.objects.create(username='u1')
        # Create 5 more twicles than the minimum to display
        self.create_twicles(u1, defaults.twicles_per_page_min_value + 5)
        # Request less than all available
        amount = defaults.twicles_per_page_min_value + 1
        self.assertLessEqual(
            len(retrieve_subscribed_twicles(u1.username, amount)),
            amount)
        # Request more than all available
        amount = defaults.twicles_per_page_min_value + 10
        self.assertLessEqual(
            len(retrieve_subscribed_twicles(u1.username, amount)),
            amount)

    def test_user_gets_her_following_twicles_only(self):
        """
        Checks that the twicles returned for <user>:
            Include her own twicles
            Include twicles of people she's following
            Do NOT include twicles of people she's NOT following
        :return:
        """
        # Create 2 users
        user1 = User.objects.create(username='u1')
        user2 = User.objects.create(username='u2')
        user3 = User.objects.create(username='u3')

        # user1 starts following user2
        user1.following.add(user2)

        # user1 publishes some twicles
        twicles_user1 = self.create_twicles(user1, 5)

        # user2 publishes some twicles
        twicles_user2 = self.create_twicles(user2, 5)

        # user3 publishes some twicles
        twicles_user3 = self.create_twicles(user3, 5)

        # check that only user1 and user2 twicles are returned
        #   in no particular order
        self.assertQuerysetEqual(retrieve_subscribed_twicles(user1.username),
                                 [twicle.id
                                  for twicle
                                  in twicles_user1 + twicles_user2],
                                 ordered=False,
                                 transform=lambda obj: obj.id)

        # def test_raise_404_if_user_with_provided_username_does_not_exist(self):
        # QUESTION: Esto no se puede testear acá :/
        # https://docs.djangoproject.com/en/1.7/topics/testing/tools/#exceptions

        #self.assertRaises(Http404, retrieve_subscribed_twicles('nonexistent'))


class HomeViewTests(TestCase):

    def create_user(self, username):
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

    def get_response_with_authenticated_user(self):
        u = self.create_user('test')
        # Log the user in
        self.client.login(username=u.username, password=u.username)
        # Get the home page
        return u, self.client.get(reverse('home'))

    def test_anonymous_user_gets_redirected(self):
        rsp = self.client.get(reverse('home'))
        self.assertEquals(rsp.status_code, 302)

    def test_authenticated_user_gets_http_200(self):
        user, rsp = self.get_response_with_authenticated_user()
        self.assertEquals(rsp.status_code, 200)

    def test_context_elements_that_should_always_be_passed_to_template(self):
        user, rsp = self.get_response_with_authenticated_user()
        # profile context variable should be
        #   the user object that made the request
        self.assertEquals(rsp.context['profile'], user)
        self.assertIn('twicles', rsp.context.keys())
        self.assertIsInstance(rsp.context['followers_count'], int)
        self.assertIsInstance(rsp.context['following_count'], int)
        self.assertIsInstance(rsp.context['new_twicle_form'],
                              forms.NewTwicleForm)
        self.assertIsInstance(rsp.context['profile_form'],
                              users.forms.ProfileForm)
        self.assertIsInstance(rsp.context['edit_tags_form'],
                              users.forms.ProfileTagsForm)
        self.assertIsInstance(rsp.context['new_tag_form'],
                              users.forms.TagForm)