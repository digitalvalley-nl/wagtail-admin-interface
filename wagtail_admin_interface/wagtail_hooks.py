# Python Standard Library
import json

# Django
from django.conf import settings
from django.contrib.auth.models import Permission
from django.utils.safestring import mark_safe

# Wagtail
from wagtail import hooks
from wagtail.models import Page


@hooks.register('construct_main_menu')
def construct_main_menu(request, menu_items):
    if not hasattr(settings, 'WAGTAIL_ADMIN_INTERFACE'):
        return

    # Hide main menu items that are not whitelisted
    if 'HIDDEN_MAIN_MENU_ITEMS' in settings.WAGTAIL_ADMIN_INTERFACE \
            and settings.WAGTAIL_ADMIN_INTERFACE['HIDDEN_MAIN_MENU_ITEMS'] is not None:
        menu_items[:] = [menu_item for menu_item in menu_items if menu_item.name not in settings.WAGTAIL_ADMIN_INTERFACE['HIDDEN_MAIN_MENU_ITEMS']]


@hooks.register('construct_settings_menu')
def construct_settings_menu(request, menu_items):
    if not hasattr(settings, 'WAGTAIL_ADMIN_INTERFACE'):
        return

    # Hide settings menu items that are not whitelisted
    if 'HIDDEN_SETTINGS_MENU_ITEMS' in settings.WAGTAIL_ADMIN_INTERFACE \
            and settings.WAGTAIL_ADMIN_INTERFACE['HIDDEN_SETTINGS_MENU_ITEMS'] is not None:
        menu_items[:] = [menu_item for menu_item in menu_items if menu_item.name not in settings.WAGTAIL_ADMIN_INTERFACE['HIDDEN_SETTINGS_MENU_ITEMS']]


@hooks.register('insert_global_admin_js')
def insert_global_admin_js():
    data = {}

    if not hasattr(settings, 'WAGTAIL_ADMIN_INTERFACE'):
        return

    # Hide group object permisions that are not whitelisted
    if 'HIDDEN_GROUP_OBJECT_PERMISSIONS' in settings.WAGTAIL_ADMIN_INTERFACE \
            and settings.WAGTAIL_ADMIN_INTERFACE['HIDDEN_GROUP_OBJECT_PERMISSIONS'] is not None:
        permissions = Permission.objects.filter(content_type__model__in=settings.WAGTAIL_ADMIN_INTERFACE['HIDDEN_GROUP_OBJECT_PERMISSIONS'])
        data['HIDDEN_GROUP_OBJECT_PERMISSIONS'] = [permission.id for permission in permissions]

    return mark_safe('<script>const WagtailAdminInterface = ' + json.dumps(data)  + ';</script>')
