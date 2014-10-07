# coding=utf-8
from django.contrib import admin
from django.contrib.auth import get_user_model

from twicles.models import Twicle, UserSettings
User = get_user_model()


class TwicleIncludesImageFilter(admin.SimpleListFilter):
    """
    Filters the Twicle list depending on what the includes_image method returns
    """
    title = "Includes image?"

    parameter_name = 'includes_image'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('yes', 'yes'),
            ('no', 'no'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'yes':
            return queryset.exclude(image__exact='')
        if self.value() == 'no':
            return queryset.filter(image__exact='')


@admin.register(Twicle)
class AdminTwicle(admin.ModelAdmin):

    def includes_image(self, obj):
        """
        returns True if the twicle has an image or False if it's
        not present
        :return:    boolean
        """
        return bool(obj.image)

    includes_image.boolean = True
    includes_image.short_description = "Tiene imagen?"

    date_hierarchy = 'created'
    list_display = ('text', 'author', 'created', 'includes_image')
    list_filter = ('author', 'created', TwicleIncludesImageFilter)
    search_fields = ('text', 'author__username')


admin.site.register(UserSettings)
