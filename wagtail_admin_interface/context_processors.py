# Django
from django.conf import settings as django_settings


def settings(request):
    context = {}
    if hasattr(django_settings, 'WAGTAIL_ADMIN_INTERFACE'):
        context['WAGTAIL_ADMIN_INTERFACE'] = django_settings.WAGTAIL_ADMIN_INTERFACE

        if 'SINGLE_SITE' in django_settings.WAGTAIL_ADMIN_INTERFACE:
            context['WAGTAIL_ADMIN_INTERFACE']['SINGLE_SITE']['HOME_PAGE_URL'] = \
                '/pages/' + str(django_settings.WAGTAIL_ADMIN_INTERFACE['SINGLE_SITE']['HOME_PAGE_ID']) + '/'

            if 'LAYOUT_PAGE_ID' in django_settings.WAGTAIL_ADMIN_INTERFACE['SINGLE_SITE']:
                context['WAGTAIL_ADMIN_INTERFACE']['SINGLE_SITE']['LAYOUT_PAGE_URL'] = \
                    '/pages/' + str(django_settings.WAGTAIL_ADMIN_INTERFACE['SINGLE_SITE']['LAYOUT_PAGE_ID']) + '/'

    return context
