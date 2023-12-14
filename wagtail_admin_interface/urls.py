# Django
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path

# Wagtail
from wagtail.admin.views.pages.listing import IndexView


class WagtailAdminInterfaceIndexView(IndexView):
    def get(self, request, parent_page_id=None):
        if hasattr(settings, 'WAGTAIL_ADMIN_INTERFACE') \
                and 'SINGLE_SITE' in settings.WAGTAIL_ADMIN_INTERFACE:
            home_page_url = '/pages/' + str(settings.WAGTAIL_ADMIN_INTERFACE['SINGLE_SITE']['HOME_PAGE_ID']) + '/'
            return HttpResponseRedirect(home_page_url)

        return super().get(request, parent_page_id)


urlpatterns = [
    path("pages/", WagtailAdminInterfaceIndexView.as_view(), name="wagtailadmin_explore_root"),
    path("pages/1/", WagtailAdminInterfaceIndexView.as_view(), name="wagtailadmin_explore_root")
]
