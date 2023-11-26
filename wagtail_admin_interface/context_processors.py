# Django
from django.conf import settings as django_settings


def settings(request):
    context = {}
    if hasattr(django_settings, 'WAGTAIL_ADMIN_INTERFACE'):
        context['WAGTAIL_ADMIN_INTERFACE'] = django_settings.WAGTAIL_ADMIN_INTERFACE
    return context
