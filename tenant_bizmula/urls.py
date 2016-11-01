from django.conf.urls import include, url
from tenant_bizmula.views import stage_view, module_view


urlpatterns = (
    # EXERCISES

    # MODULES
    url(r'^bizmula/module/(.*)/(.*)/$', module_view.detail_page, name='tenant_bizmula_module_detail'),
    url(r'^bizmula/module/(.*)/$', module_view.master_page, name='tenant_bizmula_module_master'),

    # MODULES
    url(r'^bizmula/modules$', stage_view.master_page, name='tenant_bizmula_modules_master'),
)
