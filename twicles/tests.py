# coding=utf-8
from django.test import TestCase
from django.http import Http404


from twicles.api import retrieve_subscribed_twicles
from twicles.models import Twicle
from django.contrib.auth import get_user_model
User = get_user_model()


class ApiRetrieveSubscribedTwiclesTests(TestCase):

    def test_user_without_twicles_or_following_returns_empty_queryset(self):
        u1 = User.objects.create(username='u1', bio='bio')

        self.assertQuerysetEqual(retrieve_subscribed_twicles(u1.username),
                                 User.objects.none())  # Compare to empty QS

    def test_returns_as_many_twicles_as_amount_or_less(self):
        u1 = User.objects.create(username='u1', bio='bio')

        # Create 2 twicles
        Twicle.objects.create(text='twicleu1', author=u1)
        Twicle.objects.create(text='twicleu2', author=u1)

        # Less than available
        amount = 1
        self.assertLessEqual(len(retrieve_subscribed_twicles(u1.username,
                                                             amount)),
                             amount)

        # None TODO: This should not be allowed
        amount = 0
        self.assertLessEqual(len(retrieve_subscribed_twicles(u1.username,
                                                             amount)),
                             amount)

        # More than available
        amount = 10
        self.assertLessEqual(len(retrieve_subscribed_twicles(u1.username,
                                                             amount)),
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
        user1 = User.objects.create(username='u1', bio='bio')
        user2 = User.objects.create(username='u2', bio='bio')
        user3 = User.objects.create(username='u3', bio='bio')

        # user1 starts following user2
        user1.following.add(user2)

        # user1 publishes some twicles
        twicles_user1 = [Twicle.objects.create(text='twicle' + str(n) + 'u1',
                                               author=user1)
                         for n in range(5)]

        # user2 publishes some twicles
        twicles_user2 = [Twicle.objects.create(text='twicle' + str(n) + 'u2',
                                               author=user2)
                         for n in range(5)]

        # user3 publishes some twicles
        twicles_user3 = [Twicle.objects.create(text='twicle' + str(n) + 'u3',
                                               author=user3)
                         for n in range(5)]

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