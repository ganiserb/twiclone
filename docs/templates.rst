base_twicle_list
================

receives:

    var name            type
    --------            ----
    twicles             iterable of Twicle          used to show the twicles provided as a list
    profile             Profile instance            used to show the user profile
    interest_tags       iterable of InterestTag     used to display a list of the user interests - Only if edition_allowed != True
    edition_allowed     boolean                     if True, shows the controls and forms to edit the profile
    profile_form        users.forms.ProfileForm     for editing the profile
    edit_tags_form      users.forms.ProfileTagsForm for editing the user's list of interest tags
    new_tag_form        users.forms.TagForm         for adding interest tags to the available choices
    followers_count
    following_count


home
====

receives:
    base_twicle_list

    new_twicle_form     twicles.forms.NewTwicleForm for posting a new Twicle


view_user_twicles
=================

