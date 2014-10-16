# coding=utf-8
from django.test import TestCase
from mock import MagicMock, patch
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse

from twicles.api import retrieve_subscribed_twicles, retrieve_user_twicles
from twicles import defaults, forms
from tests import utils
import users
from twicles import views
from django.contrib.auth import get_user_model
User = get_user_model()


class CommonRetrieveTests(object):
    """
    Common tests for the retrieve api functions
    """
    function = None

    def test_amount_parameter_raises_value_error_if_amount_less_than_minimum(self):
        """
        tests that the api function raises a value error when the
        amount parameter is less than the minimum defined by default
        """
        u1 = User.objects.create(username='u1')
        self.assertRaises(ValueError,
                          self.function,
                          username=u1.username,
                          amount=(defaults.twicles_per_page_min_value - 1))

    def test_amount_parameter_raises_value_error_if_amount_negative(self):
        """
        tests that the api function raises a value error when the
        amount parameter is negative
        """
        u1 = User.objects.create(username='u1')
        self.assertRaises(ValueError,
                          self.function,
                          username=u1.username,
                          amount=(-defaults.twicles_per_page_min_value))

    def test_returns_as_many_twicles_as_amount_or_less(self):
        u1 = User.objects.create(username='u1')
        # Create 5 more twicles than the minimum to display
        utils.create_twicles(u1, defaults.twicles_per_page_min_value + 5)
        # Request less than all available
        amount = defaults.twicles_per_page_min_value + 1
        self.assertLessEqual(
            len(self.function(u1.username, amount)),
            amount)
        # Request more than all available
        amount = defaults.twicles_per_page_min_value + 10
        self.assertLessEqual(
            len(self.function(u1.username, amount)),
            amount)

    def test_retrieving_nonexistent_user_raises_404(self):
        self.assertRaises(Http404, self.function, 'nonexistent')


class ApiRetrieveSubscribedTwiclesTests(TestCase, CommonRetrieveTests):

    def setUp(self):
        self.function = retrieve_subscribed_twicles

    def test_user_without_twicles_and_without_following_returns_empty_queryset(self):
        u1 = User.objects.create(username='u1')
        self.assertQuerysetEqual(retrieve_subscribed_twicles(u1.username),
                                 User.objects.none())  # Compare to empty QS

    def test_user_gets_her_following_twicles_only(self):
        """
        Checks that the twicles returned for <user>:
            Include her own twicles
            Include twicles of people she's following
            Do NOT include twicles of people she's NOT following
        :return:
        """
        # Create 3 users
        user1 = User.objects.create(username='u1')
        user2 = User.objects.create(username='u2')
        user3 = User.objects.create(username='u3')

        # user1 starts following user2
        user1.following.add(user2)

        # user1 publishes some twicles
        twicles_user1 = utils.create_twicles(user1, 5)

        # user2 publishes some twicles
        twicles_user2 = utils.create_twicles(user2, 5)

        # user3 publishes some twicles
        twicles_user3 = utils.create_twicles(user3, 5)

        # check that only user1 and user2 twicles are returned
        #   in no particular order
        self.assertQuerysetEqual(retrieve_subscribed_twicles(user1.username),
                                 [twicle.id
                                  for twicle
                                  in twicles_user1 + twicles_user2],
                                 ordered=False,
                                 transform=lambda obj: obj.id)

        self.assertRaises(Http404, retrieve_subscribed_twicles, 'nonexistent')


class ApiRetrieveProfileTwiclesTests(TestCase, CommonRetrieveTests):

    def setUp(self):
        self.function = retrieve_user_twicles

    def test_user_without_twicles_returns_empty_queryset(self):
        u1 = User.objects.create(username='u1')
        self.assertQuerysetEqual(self.function(u1.username),
                                 User.objects.none())  # Compare to empty QS

    def test_user_gets_the_twicles_for_the_requested_profile_only(self):
        """
        Checks that the twicles returned for <user>:
            Are twicles published ONLY by <user>
            Do not include twicles of people <user> is following
            Do NOT include twicles of people <user> is NOT following
        :return:
        """
        # Create 3 users
        user1 = User.objects.create(username='u1')
        user2 = User.objects.create(username='u2')
        user3 = User.objects.create(username='u3')

        # user1 starts following user2
        user1.following.add(user2)

        # user1 publishes some twicles
        twicles_user1 = utils.create_twicles(user1, 5)

        # user2 publishes some twicles
        twicles_user2 = utils.create_twicles(user2, 5)

        # user3 publishes some twicles
        twicles_user3 = utils.create_twicles(user3, 5)

        # check that only user1 twicles are returned
        #   in no particular order
        self.assertQuerysetEqual(self.function(user1.username),
                                 [twicle.id
                                  for twicle
                                  in twicles_user1],
                                 ordered=False,
                                 transform=lambda obj: obj.id)

#
# class CommonViewTests(object):
#     view = None
#     url = None
#     retrieve_function = None
#
#     def test_view_gets_twicles_from_retrieve_function(self):
#         retrieve_function_mock = MagicMock()
#         json_response_mock = MagicMock()
#
#         retrieve_function_mock.return_value = ['test']
#
#         json_response_mock.return_value = HttpResponse()
#
#         with patch(self.retrieve_function, new=retrieve_function_mock), \
#              patch('siteapi.views.JsonResponse', new=json_response_mock):
#             # With these two functions patched, we can now call the view
#             #   (but authenticated, so it works for both views)
#
#             user, rsp = utils.get_response_with_authenticated_user(
#                 self.client,
#                 self.url
#             )
#
#             self.assertTrue(retrieve_function_mock.called)
#             self.assertEquals(retrieve_function_mock.call_count, 1)


class HomeViewTests(TestCase):#, CommonViewTests):

    def setUp(self):
        self.retrieve_function = 'twicles.views.retrieve_subscribed_twicles'
        self.view = views.home
        self.url = reverse('home')

    def test_anonymous_user_gets_redirected(self):
        rsp = self.client.get(reverse('home'))
        self.assertEquals(rsp.status_code, 302)

    def test_authenticated_user_gets_http_200(self):
        user, rsp = utils.get_response_with_authenticated_user(self.client,
                                                               reverse('home'))
        self.assertEquals(rsp.status_code, 200)

    def test_context_elements_that_should_always_be_passed_to_template(self):
        user, rsp = utils.get_response_with_authenticated_user(self.client,
                                                               reverse('home'))
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


# class ProfileViewTests(TestCase, CommonViewTests):
#     raise NotImplementedError