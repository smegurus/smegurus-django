from django.conf.urls import patterns, include, url
from tenant_message import views


urlpatterns = (
    url(r'^message$', views.inbox_page, name='tenant_message_inbox'),
    url(r'^message/composer/(.*)/$', views.specific_compose_page, name='tenant_message_specific_composer'),
    url(r'^message/composer$', views.compose_page, name='tenant_message_composer'),
    url(r'^message/archive/(.*)/$', views.archive_conversation_page, name='tenant_archive_conversation'),
    url(r'^message/(.*)/$', views.conversation_page, name='tenant_conversation'),
    url(r'^archive$', views.archive_list_page, name='tenant_archive_inbox'),
    url(r'^archive/(.*)/$', views.archive_details_page, name='tenant_archive_details'),
)
