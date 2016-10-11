from django.conf.urls import include, url
from foundation_email import views


urlpatterns = (
    url(r'^email/task/(.*)/(.*)/$', views.task_page, name='foundation_email_task'),
    url(r'^email/intake/pending/(.*)/$', views.pending_intake_page, name='foundation_email_pending_intake'),
    url(r'^email/intake/approved/(.*)/$', views.approved_intake_page, name='foundation_email_approved_intake'),
    url(r'^email/intake/rejected/(.*)/$', views.rejected_intake_page, name='foundation_email_rejected_intake'),
    url(r'^email/message/(.*)/$', views.message_page, name='foundation_email_message'),
    url(r'^email/calendar/pending/(.*)/$', views.calendar_pending_event_page, name='foundation_email_calendar_pending_event')
)
