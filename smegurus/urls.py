"""bizmula URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url('^', include('django.contrib.auth.urls')),
    url(r'^', include('api.urls')),
]

urlpatterns += i18n_patterns(
    url(r'^', include('foundation_public.urls')),
    url(r'^', include('landpage.urls')),
    url(r'^', include('foundation_auth.urls')),
    url(r'^', include('foundation_config.urls')),
    url(r'^', include('tenant_profile.urls')),
    url(r'^', include('tenant_message.urls')),
    url(r'^', include('tenant_calendar.urls')),
    url(r'^', include('tenant_community.urls')),
    url(r'^', include('tenant_goal.urls')),
    url(r'^', include('tenant_learning.urls')),
    url(r'^', include('tenant_mywork.urls')),
    url(r'^', include('tenant_progress.urls')),
    url(r'^', include('tenant_resource.urls')),
    url(r'^', include('tenant_reward.urls')),
    url(r'^', include('tenant_intake.urls')),
    url(r'^', include('tenant_dashboard.urls')),
)
