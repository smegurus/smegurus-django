from django.conf.urls import patterns, include, url
from tenant_reception.views import dashboard_view, decorator_view, todo_view


urlpatterns = (
    url(r'^reception/is_required$', decorator_view.is_required_page, name='tenant_reception_is_required'),
    url(r'^reception/todo$', todo_view.reception_todo_master_page, name='tenant_reception_todo'),
    url(r'^reception$', dashboard_view.reception_dashboard_master_page, name='tenant_reception'),
)
