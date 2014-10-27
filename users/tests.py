# coding=utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse
from mock import MagicMock, patch

from twicles.forms import NewTwicleForm
from tests import utils
import users
from django.contrib.auth import get_user_model
User = get_user_model()


class ShowProfileViewTests(TestCase):

    def test_status_code_always_200(self):
        u = utils.create_user('test')

        # anonymous request
        rsp = self.client.get(reverse('users:show_profile',
                                      kwargs={'username': u.username}))
        self.assertEquals(rsp.status_code, 200)

        # authenticated request
        request_user, rsp = utils.get_response_with_authenticated_user(
            self.client,
            reverse('users:show_profile', kwargs={'username': u.username})
        )
        self.assertEquals(rsp.status_code, 200)

    def test_correct_context_variables_passed_to_template(self):
        u = utils.create_user('test')
        request_user, rsp = utils.get_response_with_authenticated_user(
            self.client,
            reverse('users:show_profile', kwargs={'username': u.username})
        )

        # profile context variable should be
        #   the user object that made the request
        self.assertEquals(rsp.context['profile'], u)
        self.assertIn('twicles', rsp.context.keys())
        self.assertIn('display_unfollow', rsp.context.keys())
        self.assertIsInstance(rsp.context['followers_count'], int)
        self.assertIsInstance(rsp.context['following_count'], int)
        self.assertIsInstance(rsp.context['new_twicle_form'], NewTwicleForm)

    def test_anonymous_user_does_not_see_follow_control_link(self):
        u = utils.create_user('test')   # Create the user to request her profile

        rsp = self.client.get(reverse('users:show_profile',
                                      kwargs={'username': u.username}))

        # Check that she does not see the follow link
        self.assertNotIn('<a id="follow_control_button" href="#">',
                         rsp.content.decode('utf-8'))

    def test_authenticated_user_sees_follow_link(self):
        u = utils.create_user('test')
        user, rsp = utils.get_response_with_authenticated_user(
            self.client,
            reverse('users:show_profile', kwargs={'username': u.username}),
        )
        self.assertIn('follow_control_action="f";',  # Check this way because JS
                      rsp.content.decode('utf-8'))

    def test_authenticated_user_sees_unfollow_link(self):
        u = utils.create_user('test')
        o = utils.create_user('pepe')
        o.following.add(u)
        user, rsp = utils.get_response_with_authenticated_user(
            self.client,
            reverse('users:show_profile', kwargs={'username': u.username}),
            user=o
        )
        self.assertIn('follow_control_action="u";',  # Check this way because JS
                      rsp.content.decode('utf-8'))

    def test_authenticated_user_does_not_see_follow_control_on_her_own_profile(self):
        u = utils.create_user('test')
        user, rsp = utils.get_response_with_authenticated_user(
            self.client,
            reverse('users:show_profile', kwargs={'username': u.username}),
            user=u
        )
        self.assertNotIn('<a id="follow_control_button" href="#">',
                         rsp.content.decode('utf-8'))

    def test_nonexisting_username_returns_404(self):
        rsp = self.client.get(reverse('users:show_profile',
                                      kwargs={'username': 'inexistente'}))
        self.assertEquals(rsp.status_code, 404)

    def test_new_twicle_form_includes_at_username(self):
        """
        Checks that twicle posting form in the profile view
        is filled with @username, where <username> is the name
        of the user whose profile is shown
        """
        # create a user to have a profile to show
        u = utils.create_user('test')
        # anonymous user makes the request
        rsp = self.client.get(reverse('users:show_profile',
                                      kwargs={'username': u.username}))
        self.assertIn('@' + u.username,
                      rsp.context['new_twicle_form'].initial['text'])

    def test_view_calls_retrieve_function_properly(self):
        retrieve_function_mock = MagicMock()
        mock = MagicMock()
        defaults_mock = MagicMock()
        defaults_mock.twicles_per_page = 100
        request_mock = MagicMock()
        user_settings_mock = MagicMock()

        user_mock = MagicMock()
        user_mock.username = 'utest'

        get_user_mock = MagicMock(return_value=user_mock)

        with patch('users.views.retrieve_user_twicles',
                   new=retrieve_function_mock),\
             patch('users.views.UserSettings',
                   new=user_settings_mock), \
             patch('users.views.render', new=mock),\
             patch('users.views.defaults', new=defaults_mock),\
             patch('users.views.get_object_or_404', new=get_user_mock):

            request_mock.user.is_authenticated.return_value = False

            users.views.show_profile(request_mock, 'utest')
            # Unauthenticated... The amount is the mock that mocks the defaults
            retrieve_function_mock.assert_called_once_with(user_mock.username,
                                                           100,
                                                           requester=None)

            user_settings_mock.objects.get().twicles_per_page = 100
            request_mock.user.is_authenticated.return_value = True
            users.views.show_profile(request_mock, 'utest')
            # Authenticated... The amount is the value from the user settings
            retrieve_function_mock.assert_called_with('utest',
                                                       100,
                                                       requester=request_mock.user)


class PostFormViewCommon(object):

    view = None
    form_path = None

    def test_view_redirects_somewhere_if_method_is_not_post(self):
        redirect = MagicMock()
        request = MagicMock()

        with patch(self.form_path, new=MagicMock),\
             patch('users.views.get_object_or_404', new=MagicMock),\
             patch('users.views.HttpResponseRedirect', new=redirect):
             self.view(request)

        self.assertEquals(redirect.call_count, 1)

    # QUESTION: Cómo no repetir el código de los sig tests?
    def test_view_redirects_to_next_field_on_valid_form(self):
        request = MagicMock()
        request.method = 'POST'
        request.user.is_authenticated.return_value = True   # Bypass @login_req

        form = MagicMock()
        form.return_value = form    # DO NOT return a new mock instance!
        form.is_valid.return_value = True
        form.cleaned_data['next'] = 'url'

        # The user whose profile will be edited
        #   (retrieved with get_object_or_404)
        get_user_from_form = MagicMock()
        # In case the view retrieves a user
        get_user_from_form.return_value = request.user

        redirect = MagicMock()

        with patch(self.form_path, new=form),\
             patch('users.views.get_object_or_404', new=get_user_from_form),\
             patch('users.views.HttpResponseRedirect', new=redirect):
            self.view(request)

        redirect.assert_called_once_with(form.cleaned_data['next'])

    def test_view_saves_posted_data_on_valid_form(self):
        request = MagicMock()
        request.method = 'POST'
        request.user.is_authenticated.return_value = True   # Bypass @login_req

        form = MagicMock()
        form.return_value = form    # DO NOT return a new mock instance!
        form.is_valid.return_value = True

        get_user_from_form = MagicMock()
        get_user_from_form.return_value = request.user

        with patch(self.form_path, new=form),\
             patch('users.views.get_object_or_404', new=get_user_from_form),\
             patch('users.views.HttpResponseRedirect', new=MagicMock()):
            self.view(request)

        self.assertEquals(form.save.call_count, 1)

    def test_view_saves_request_info_in_session_on_invalid_form(self):
        request = MagicMock()
        request.method = 'POST'
        request.POST.copy.return_value = 'data'
        request.user.is_authenticated.return_value = True   # Bypass @login_req
        request.session = {}

        form = MagicMock()
        form.return_value = form    # DO NOT return a new mock instance!
        form.is_valid.return_value = False

        # The user whose profile will be edited
        #   (retrieved with get_object_or_404)
        get_user_from_form = MagicMock()
        get_user_from_form.return_value = request.user

        redirect = MagicMock()

        with patch(self.form_path, new=form),\
             patch('users.views.get_object_or_404', new=get_user_from_form),\
             patch('users.views.HttpResponseRedirect', new=redirect):
            self.view(request)

        self.assertIn('data',
                      request.session.values())


class PostProfileFormViewTests(TestCase, PostFormViewCommon):

    def setUp(self):
        self.view = users.views.post_profile_form
        self.form_path = 'users.views.ProfileForm'


class PostNewTagFormTests(TestCase, PostFormViewCommon):

    def setUp(self):
        self.view = users.views.post_new_tag_form
        self.form_path = 'users.views.TagForm'


class PostEditTagsForm(TestCase, PostFormViewCommon):

    def setUp(self):
        self.view = users.views.post_edit_tags_form
        self.form_path = 'users.views.ProfileTagsForm'