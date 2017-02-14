from django.conf.urls import include, url
from foundation_tenant.views import s3_views


urlpatterns = (
    # Simple Storage Service
    url(r'^s3file/(.*)/get_timed_url$', s3_views.s3file_timed_url, name='foundation_s3file_60_sec_timed_url'),
    url(r'^s3file/(.*)/delete$', s3_views.delete_s3file, name='foundation_delete_s3file')
)
