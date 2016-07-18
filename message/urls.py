from django.conf.urls import patterns, include, url
from message import views


urlpatterns = (
    url(r'^message/inbox$', views.message_inbox_page, name='tenant_message_inbox'),
    url(r'^message/composer$', views.message_compose_page, name='tenant_message_composer'),
    # url(r'^tenant/is_valid$', decoratorsview.tenant_is_valid, name='tenant_is_valid'),
    # url(r'^group/is_entrepreneur$', decoratorsview.group_is_entrepreneur, name='group_is_entrepreneur'),
    # url(r'^group/is_org_admin$', decoratorsview.group_is_org_admin, name='group_is_org_admin'),
)
