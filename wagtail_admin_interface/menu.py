# Django
from django.conf import settings

# Wagtail
from wagtail.admin.menu import MenuItem


class LayoutMenuItem(MenuItem):

    def __init__(self):
        url = None
        if hasattr(settings, 'WAGTAIL_ADMIN_INTERFACE') \
                and 'SINGLE_SITE' in settings.WAGTAIL_ADMIN_INTERFACE \
                and 'LAYOUT_PAGE_ID' in settings.WAGTAIL_ADMIN_INTERFACE['SINGLE_SITE']:
            url = '/pages/' + str(
                settings.WAGTAIL_ADMIN_INTERFACE['SINGLE_SITE']['LAYOUT_PAGE_ID']
            ) + '/edit/'
        super().__init__('Layout', url, icon_name='globe', order=0)

    def is_shown(self, request):
        if self.url is None:
            return False
        return True
