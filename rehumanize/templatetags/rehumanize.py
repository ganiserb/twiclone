# coding=utf-8
__author__ = 'gabriel'
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def rehumanize(value):
    cosa = value.replace('\\u00a0', ' ')
    return cosa