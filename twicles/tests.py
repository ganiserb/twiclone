# coding=utf-8
from django.test import TestCase
from mock import MagicMock, patch
from django.core.urlresolvers import reverse
from django.http import Http404

from twicles.api import retrieve_subscribed_twicles, retrieve_user_twicles
from twicles import defaults, forms, models, views
from tests import utils
from users.tests import PostFormViewCommon
import users
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
        user4 = User.objects.create(username='u4')

        # user1 starts following user2
        user1.following.add(user2)

        # user1 publishes some twicles
        twicles_user1 = utils.create_twicles(user1, 5)

        # user2 publishes some twicles
        utils.create_twicles(user2, 5)

        # user2 is concerned about privacy, so he doesn't want everyone seen his
        #   twicles:
        user2.usersettings.visibility = models.UserSettings.FOLLOWING
        user2.usersettings.save()

        # user3 publishes some twicles
        twicles_user3 = utils.create_twicles(user3, 5)

        # user1 starts following user3 because user2 disappeared
        user1.following.add(user3)

        # user4 publishes some twicles, but nobody notices...
        utils.create_twicles(user4, 5)

        # check that only user1 and user2 twicles are returned
        #   in no particular order
        self.assertQuerysetEqual(retrieve_subscribed_twicles(user1.username),
                                 [twicle.id
                                  for twicle
                                  in twicles_user1 + twicles_user3],
                                 ordered=False,
                                 transform=lambda obj: obj.id)


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

    def test_private_twicles_not_returned_without_requester(self):
        u1 = utils.create_user('user1')
        utils.create_twicles(u1, 5)
        u1.usersettings.visibility = models.UserSettings.FOLLOWING
        u1.usersettings.save()

        self.assertQuerysetEqual(self.function(u1.username),
                                 models.Twicle.objects.none())

    def test_private_twicles_not_returned_without_requester_being_followed(self):
        u1 = utils.create_user('user1')
        utils.create_twicles(u1, 5)
        u1.usersettings.visibility = models.UserSettings.FOLLOWING
        u1.usersettings.save()

        u2 = utils.create_user('requester')
        # u2 shouldn't see u1 twicles because u1 is not following her

        self.assertQuerysetEqual(self.function(u1.username, requester=u2),
                                 models.Twicle.objects.none())

    def test_private_twicles_returned_if_requester_is_being_followed(self):
        u1 = utils.create_user('user1')
        twicles_u1 = utils.create_twicles(u1, 5)
        u1.usersettings.visibility = models.UserSettings.FOLLOWING
        u1.usersettings.save()

        u2 = utils.create_user('requester')
        u1.following.add(u2)
        # u2 should see u1 twicles because u1 is following her

        self.assertQuerysetEqual(self.function(u1.username, requester=u2),
                                 [twicle.id
                                  for twicle
                                  in twicles_u1],
                                 ordered=False,
                                 transform=lambda obj: obj.id)


class HomeViewTests(TestCase):

    def setUp(self):
        self.url = reverse('home')

    def test_anonymous_user_gets_redirected(self):
        rsp = self.client.get(self.url)
        self.assertEquals(rsp.status_code, 302)

    def test_authenticated_user_gets_http_200(self):
        user, rsp = utils.get_response_with_authenticated_user(self.client,
                                                               self.url)
        self.assertEquals(rsp.status_code, 200)

    def test_context_elements_that_should_always_be_passed_to_template(self):
        user, rsp = utils.get_response_with_authenticated_user(self.client,
                                                               self.url)
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

    # QUESTION: Cómo no repetir el código de patcheo de los siguientes 2 tests que sólo difieren en el setup de los mocks?
    #       ----> Usando un callable para que sea ejecutado dentro del with
    def test_view_gets_twicles_from_retrieve_function(self):
        """
        Checks that the api function is really used for retrieving
        the view twicles
        """
        retrieve_function_mock = MagicMock()
        retrieve_function_mock.return_value = ['test']
        mock = MagicMock()

        with patch('twicles.views.retrieve_subscribed_twicles',
                   new=retrieve_function_mock),\
             patch('twicles.views.UserSettings',
                   new=mock), \
             patch('twicles.views.ProfileForm', new=mock),\
             patch('twicles.views.ProfileTagsForm', new=mock),\
             patch('twicles.views.TagForm', new=mock),\
             patch('twicles.views.NewTwicleForm', new=mock),\
             patch('twicles.views.render', new=mock):

            # Call the view directly to test later
            views.home(mock)

        self.assertTrue(retrieve_function_mock.called)
        self.assertEquals(retrieve_function_mock.call_count, 1)

    def test_view_calls_retrieve_function_properly(self):
        """
        Checks that the api functions is properly called
        """
        retrieve_function_mock = MagicMock()
        mock = MagicMock()
        request_mock = MagicMock()
        user_mock = MagicMock()
        request_mock.user = user_mock
        user_mock.is_authenticated.return_value = True  # Always in home!

        user_settings_mock = MagicMock()

        with patch('twicles.views.retrieve_subscribed_twicles',
                   new=retrieve_function_mock),\
             patch('twicles.views.UserSettings',
                   new=user_settings_mock),\
             patch('twicles.views.ProfileForm', new=mock),\
             patch('twicles.views.ProfileTagsForm', new=mock),\
             patch('twicles.views.TagForm', new=mock),\
             patch('twicles.views.NewTwicleForm', new=mock),\
             patch('twicles.views.render', new=mock):

            user_settings_mock.objects.get().twicles_per_page = 100

            # Call the view directly
            views.home(request_mock)

        retrieve_function_mock.assert_called_once_with(user_mock, 100)


class PostTwicleFormViewTests(TestCase, PostFormViewCommon):

    def setUp(self):
        self.view = views.post_twicle
        self.form_path = 'twicles.views.NewTwicleForm'
        self.response_redirect_path = 'twicles.views.HttpResponseRedirect'
        self.get_object_or_404_path = 'twicles.views.get_object_or_404'
