from django.conf.urls import patterns, include, url
from foundation_email import views


urlpatterns = (
    url(r'^email/intake/pending/(.*)/$', views.pending_intake_page, name='foundation_email_pending_intake'),
    url(r'^email/intake/approved/(.*)/$', views.approved_intake_page, name='foundation_email_approved_intake'),
    url(r'^email/intake/rejected/(.*)/$', views.rejected_intake_page, name='foundation_email_rejected_intake'),
    url(r'^email/auth/activate$', views.activate_page, name='foundation_email_activate'),
)
