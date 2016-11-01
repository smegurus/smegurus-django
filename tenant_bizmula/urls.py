from django.conf.urls import include, url
from tenant_bizmula.views import modules_view, lectures_view


urlpatterns = (
    # EXERCISES

    # LECTURES
    url(r'^bizmula/lecture/(.*)/(.*)/$', lectures_view.detail_page, name='tenant_bizmula_lecture_detail'),
    url(r'^bizmula/lecture/(.*)/$', lectures_view.master_page, name='tenant_bizmula_lecture_master'),

    # MODULES
    url(r'^bizmula/lectures$', modules_view.master_page, name='tenant_bizmula_module_master'),
)
