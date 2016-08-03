from django.conf.urls import patterns, include, url
from tenant_message import views


urlpatterns = (
    url(r'^message/inbox$', views.message_inbox_page, name='tenant_message_inbox'),
    url(r'^message/composer$', views.message_compose_page, name='tenant_message_composer'),
    url(r'^message/archive/(.*)/$', views.archive_conversation_page, name='tenant_archive_conversation'),
    url(r'^message/(.*)/$', views.conversation_page, name='tenant_conversation'),
)
