# Django
from django.conf import settings
from django.utils.html import format_html
from django.contrib.auth.models import Permission

# Wagtail
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.models import Page


@hooks.register('construct_main_menu')
def construct_main_menu(request, menu_items):
    if not hasattr(settings, 'WAGTAIL_ADMIN_INTERFACE'):
        return

    # Hide main menu items that are not whitelisted
    if 'HIDDEN_MAIN_MENU_ITEMS' in settings.WAGTAIL_ADMIN_INTERFACE \
            and settings.WAGTAIL_ADMIN_INTERFACE['HIDDEN_MAIN_MENU_ITEMS'] is not None:
        menu_items[:] = [menu_item for menu_item in menu_items if menu_item.name not in settings.WAGTAIL_ADMIN_INTERFACE['HIDDEN_MAIN_MENU_ITEMS']]


@hooks.register('register_settings_menu_item')
def register_settings_menu_item():
    if not hasattr(settings, 'WAGTAIL_ADMIN_INTERFACE'):
        return

    if 'SINGLE_SITE' in settings.WAGTAIL_ADMIN_INTERFACE:
        return MenuItem('Layout', '/pages/' + str(settings.WAGTAIL_ADMIN_INTERFACE['SINGLE_SITE']['LAYOUT_PAGE_ID']) + '/edit/', icon_name='globe', order=0)


@hooks.register('construct_settings_menu')
def construct_settings_menu(request, menu_items):
    if not hasattr(settings, 'WAGTAIL_ADMIN_INTERFACE'):
        return

    # Hide settings menu items that are not whitelisted
    hidden_settings_menu_items = []
    if 'SINGLE_SITE' in settings.WAGTAIL_ADMIN_INTERFACE:
        hidden_settings_menu_items.append('sites')
    if 'HIDDEN_SETTINGS_MENU_ITEMS' in settings.WAGTAIL_ADMIN_INTERFACE \
            and settings.WAGTAIL_ADMIN_INTERFACE['HIDDEN_SETTINGS_MENU_ITEMS'] is not None:
        hidden_settings_menu_items += settings.WAGTAIL_ADMIN_INTERFACE['HIDDEN_SETTINGS_MENU_ITEMS']
    if len(hidden_settings_menu_items) > 0:
        menu_items[:] = [menu_item for menu_item in menu_items if menu_item.name not in hidden_settings_menu_items]


@hooks.register('insert_global_admin_css')
def insert_global_admin_css():
    if not hasattr(settings, 'WAGTAIL_ADMIN_INTERFACE'):
        return

    css = []

    if 'SINGLE_SITE' in settings.WAGTAIL_ADMIN_INTERFACE:
        css.append('''
            .wagtail-admin-interface--hide-crumb-trail-toggle .w-breadcrumbs {{
              padding-inline-start: 0.75rem;
            }}
            .wagtail-admin-interface--hide-crumb-trail-toggle .w-breadcrumbs > button:first-child {{
              display: none;
            }}
            .w-breadcrumbs nav li:first-child {{
              display: none;
            }}
            .c-page-explorer__item:has([href="/pages/''' + str(settings.WAGTAIL_ADMIN_INTERFACE['SINGLE_SITE']['LAYOUT_PAGE_ID']) + '''/"]) {{
              display: none;
            }}
        ''')

    hidden_object_group_permissions = []
    if 'SINGLE_SITE' in settings.WAGTAIL_ADMIN_INTERFACE:
        hidden_object_group_permissions.append('site')
    if 'HIDDEN_GROUP_OBJECT_PERMISSIONS' in settings.WAGTAIL_ADMIN_INTERFACE \
            and settings.WAGTAIL_ADMIN_INTERFACE['HIDDEN_GROUP_OBJECT_PERMISSIONS'] is not None:
        hidden_object_group_permissions += settings.WAGTAIL_ADMIN_INTERFACE['HIDDEN_GROUP_OBJECT_PERMISSIONS']
    if len(hidden_object_group_permissions) > 0:
        permissions = Permission.objects.filter(content_type__model__in=hidden_object_group_permissions)
        selectors = []
        for permission in permissions:
            selectors.append(
                '#object-permissions-content tr:has([name="permissions"][value="' + str(permission.id) + '"])'
            )
        css.append(', '.join(selectors) + '{{ display: none; }}')


    if 'HIDE_EDITOR_TAB_BAR_IF_SINGLE_TAB' in settings.WAGTAIL_ADMIN_INTERFACE:
        css.append('''
            .w-tabs__wrapper:not(:has(.w-tabs__tab:nth-child(2))) {{
              height: 0;
            }}
        ''')

    if len(css) > 0:
        return format_html('<style>' + ' '.join(css) + '</style>')
