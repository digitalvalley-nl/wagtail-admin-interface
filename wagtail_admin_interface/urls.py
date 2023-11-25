# Django
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path

# Wagtail
from wagtail.admin.views.pages.listing import IndexView


class WagtailAdminInterfaceIndexView(IndexView):
    def get(self, request, parent_page_id=None):
        if hasattr(settings, 'WAGTAIL_ADMIN_INTERFACE') \
                and 'REDIRECT_ROOT_PAGE_TO' in settings.WAGTAIL_ADMIN_INTERFACE \
                and settings.WAGTAIL_ADMIN_INTERFACE['REDIRECT_ROOT_PAGE_TO'] is not None:
            return HttpResponseRedirect(settings.WAGTAIL_ADMIN_INTERFACE['REDIRECT_ROOT_PAGE_TO'])

        return super().get(request, parent_page_id)


urlpatterns = [
    path("pages/", WagtailAdminInterfaceIndexView.as_view(), name="wagtailadmin_explore_root"),
    path("pages/1/", WagtailAdminInterfaceIndexView.as_view(), name="wagtailadmin_explore_root")
]
