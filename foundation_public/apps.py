from django.apps import AppConfig


class FoundationPublicConfig(AppConfig):
    name = 'foundation_public'

    def ready(self):
        """
        Function will attach the following code to be run when this application
        successfully loads up.
        """
        from django.core.checks import register, Tags, Error
        # Source: https://docs.djangoproject.com/en/dev/topics/checks/#module-django.core.checks
        from django.contrib.sites.models import Site
        from foundation_public.models.organization import PublicOrganization
        from smegurus.settings import env_var

        @register(Tags.compatibility)
        def my_checks(app_configs, **kwargs):
            """
            Function will perform a battery of tests for our SMEGurus app and
            return an error using the Django system.
            """
            errors = []  # Variable holds all the errors we detected in our system.

            # Check 1: Check to make sure our 'public' schema and 'demo' tenant
            #          schemas are setup before proceeding further.
            organizations = PublicOrganization.objects.all()
            if organizations.count() < 2:
                errors.append(
                    Error(
                        'Django-Tenant not setup with Public and Tenant schema.',
                        hint='To fix this problem, simply run the command \'./manage.py setup_org\' in your console.',
                        obj=None,
                        id='foundation_public.E002',
                    )
                )

            # Check 2: Make sure our fixtures have been imported.
            site = Site.objects.get_current().domain
            if str(site) == 'example.com':
                errors.append(
                    Error(
                        'Sites not configured',
                        hint='To fix this problem, simply run the command \'./manage.py setup_fixtures\' in your console.',
                        obj=None,
                        id='foundation_public.E001',
                    )
                )

            return errors
