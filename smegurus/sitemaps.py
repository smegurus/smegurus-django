from django.contrib import sitemaps
from django.core.urlresolvers import reverse
# from foundation_public.models.organization import PublicOrganization


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['public_home', 'public_terms',]

    def location(self, item):
        return reverse(item)

# class OrganizationSitemap(sitemaps.Sitemap):
#     priority = 0.5
#     changefreq = 'monthly'
#
#     def items(self):
#         return Organization.objects.all()


# https://docs.djangoproject.com/en/1.9/ref/contrib/sitemaps/
