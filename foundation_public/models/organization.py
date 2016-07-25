from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_tenants.models import TenantMixin, DomainMixin
from foundation_public.models.abstract_thing import AbstractPublicThing
from foundation_public.models.imageupload import PublicImageUpload
from foundation_public.models.brand import PublicBrand
from foundation_public.models.contactpoint import PublicContactPoint
from foundation_public.models.geocoordinate import PublicGeoCoordinate
from foundation_public.models.language import PublicLanguage
from foundation_public.models.openinghoursspecification import PublicOpeningHoursSpecification
from foundation_public.models.postaladdress import PublicPostalAddress
from foundation_public.models.place import PublicPlace
from foundation_public import constants


class PublicOrganization(TenantMixin, AbstractPublicThing):
    """
    An organization such as a school, NGO, corporation, club, etc.

    https://schema.org/Organization
    """
    class Meta:
        app_label = 'foundation_public'
        db_table = 'biz_organizations'
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'

    # Payment Information.
    on_trial = models.BooleanField(default=False)
    paid_until =  models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
    )

    # Django-Tenant Information.
    auto_create_schema = True
    auto_drop_schema = True

    # ------------------
    # Schema Fields
    # ------------------

    # General Information.
    address = models.ForeignKey(
        PublicPostalAddress,
        help_text=_('Physical address of the item.'),
        null=True,
        blank=True,
        related_name="organization_address_%(app_label)s_%(class)s_related"
    )
    brands = models.ManyToManyField(
        PublicBrand,
        help_text=_('The brand(s) associated with a product or service, or the brand(s) maintained by an organization or business person.'),
        blank=True,
        related_name="organization_brands_%(app_label)s_%(class)s_related"
    )
    contact_point = models.ForeignKey(
        PublicContactPoint,
        help_text=_('A contact point for a person or organization'),
        null=True,
        blank=True,
        related_name="organization_contact_point_%(app_label)s_%(class)s_related"
    )
    # department = models.ForeignKey(
    #     'self',
    #     help_text=_('A relationship between an organization and a department of that organization, also described as an organization (allowing different urls, logos, opening hours). For example: a store with a pharmacy, or a bakery with a cafe.'),
    #     null=True,
    #     blank=True,
    #     related_name="organization_department_%(app_label)s_%(class)s_related"
    # )
    dissolution_date = models.DateField(
        _("Dissolution Date"),
        help_text=_('The date that this organization was dissolved.'),
        blank=True,
        null=True
    )
    duns = models.CharField(
        _("Additional Name"),
        max_length=127,
        help_text=_('The Dun & Bradstreet DUNS number for identifying an organization or business person.'),
        blank=True,
        null=True,
    )
    email = models.EmailField(
        _("Email"),
        help_text=_('Email address.'),
        null=True,
        blank=True
    )
    fax_number = models.CharField(
        _("Fax Number"),
        max_length=31,
        help_text=_('The fax number.'),
        blank=True,
        null=True,
    )
    founding_date = models.DateField(
        _("Founding Date"),
        help_text=_('The date that this organization was founded.'),
        blank=True,
        null=True
    )
    founding_location = models.ForeignKey(
        PublicPlace,
        help_text=_('The place where the Organization was founded.'),
        null=True,
        blank=True,
        related_name="organization_founding_location_%(app_label)s_%(class)s_related"
    )
    global_location_number = models.CharField(
        _("Global Location Number"),
        max_length=255,
        help_text=_('The <a href="http://www.gs1.org/gln">Global Location Number</a> (GLN, sometimes also referred to as International Location Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit number used to identify parties and physical locations.'),
        blank=True,
        null=True,
    )
    isic_v4 = models.CharField(
        _("ISIC V4"),
        max_length=255,
        help_text=_('The International Standard of Industrial Classification of All Economic Activities (ISIC), Revision 4 code for a particular organization, business person, or place.'),
        blank=True,
        null=True,
    )
    legal_name = models.CharField(
        _("Legal Name"),
        max_length=255,
        help_text=_('The official name of the organization, e.g. the registered company name.'),
        blank=True,
        null=True,
    )
    logo = models.ForeignKey(
        PublicImageUpload,
        help_text=_('An associated logo.'),
        null=True,
        blank=True,
        related_name="organization_logo_%(app_label)s_%(class)s_related"
    )
    naics = models.CharField(
        _("NAICS"),
        max_length=127,
        help_text=_('The North American Industry Classification System (NAICS) code for a particular organization or business person.'),
        blank=True,
        null=True,
    )
    # parent_organization = models.ForeignKey(
    #     'self',
    #     help_text=_('The larger organization that this organization is a branch of, if any. Supersedes branchOf.'),
    #     null=True,
    #     blank=True,
    #     related_name="organization_parent_%(app_label)s_%(class)s_related"
    # )
    tax_id = models.CharField(
        _("Tax ID"),
        max_length=255,
        help_text=_('The Tax / Fiscal ID of the organization or person, e.g. the TIN in the US or the CIF/NIF in Spain.'),
        blank=True,
        null=True,
    )
    telephone = models.CharField(
        _("Telephone"),
        max_length=31,
        help_text=_('The telephone number.'),
        blank=True,
        null=True,
    )
    vat_id = models.CharField(
        _("Tax ID"),
        max_length=255,
        help_text=_('The Value-added Tax ID of the organization or person.'),
        blank=True,
        null=True,
    )
    users = models.ManyToManyField(
        User,
        help_text=_('The users that belong to this Organization.'),
        blank=True,
        related_name='organization_users_%(app_label)s_%(class)s_related',
    )

    # ------------------
    # Non-Schema Fields
    # ------------------

    # Metric
    how_many_served = models.PositiveSmallIntegerField(
        _("How many entrepreneurs served"),
        help_text=_('Pick the choice which best describes how many entrepreneurs are served.'),
        choices=constants.HOW_MANY_SERVED_OPTIONS,
    )
    is_tos_signed = models.BooleanField(
        _("Is terms of service signed"),
        default=False
    )

    # Social Media
    twitter_url = models.URLField(
        _("Twitter"),
        null=True,
        blank=True
    )
    facebook_url = models.URLField(
        _("Facebook"),
        null=True,
        blank=True
    )
    instagram_url = models.URLField(
        _("Instagram"),
        null=True,
        blank=True
    )
    linkedin_url = models.URLField(
        _("Linkedin"),
        null=True,
        blank=True
    )
    github_url = models.URLField(
        _("GitHub"),
        null=True,
        blank=True
    )
    google_plus_url = models.URLField(
        _("Google Plus"),
        null=True,
        blank=True
    )
    youtube_url = models.URLField(
        _("Instagram"),
        null=True,
        blank=True
    )
    flickr_url = models.URLField(
        _("Flickr"),
        null=True,
        blank=True
    )
    pintrest_url = models.URLField(
        _("Pintrest"),
        null=True,
        blank=True
    )
    reddit_url = models.URLField(
        _("Reddit"),
        null=True,
        blank=True
    )
    soundcloud_url = models.URLField(
        _("Soundcloud"),
        null=True,
        blank=True
    )

    #  Application
    is_setup = models.BooleanField(
        _("Is this account setup and ready"),
        default=False,
        help_text=_('Variable controls whether the user profile has been setup.'),
    )
    learning_preference = models.PositiveSmallIntegerField(
        _("Learning Preference"),
        help_text=_('Indicates what learning preference to use.'),
        default=constants.BLENDED_LEARNING_PREFERENCE,
        choices=constants.LEARNING_PREFERENCE_OPTIONS,
    )
    challenge = models.PositiveSmallIntegerField(
        _("Challenge"),
        help_text=_('Indicates what world challenge to use.'),
        default=constants.REAL_WORLD_CHALLENGE,
        choices=constants.CHALLENGE_OPTIONS,
    )
    has_mentors = models.BooleanField(
        _("Has mentors."),
        default=True,
        help_text=_('Variable controls whether external mentors are allowed in our system.'),
    )
    has_perks = models.BooleanField(
        _("Has perks."),
        default=True,
        help_text=_('Variable controls whether perks are allowed in our system.'),
    )

    def __str__(self):
        return str(self.name)

    def reverse(self, view_name):
        """
        Reverse the URL of the request + view name for this Organization.
        """
        from django.contrib.sites.shortcuts import get_current_site # Reverse
        from django.core.urlresolvers import resolve, reverse # Reverse
        from django.contrib.sites.models import Site
        from smegurus.settings import env_var

        http_protocol = 'https://' if env_var("SECURE_SSL_REDIRECT") else 'http://'
        if self.schema_name:
            return http_protocol + self.schema_name + '.%s' % Site.objects.get_current().domain + reverse(view_name)
        else:
            return http_protocol + '%s' % Site.objects.get_current().domain + reverse(view_name)


class PublicDomain(DomainMixin):
    class Meta:
        app_label = 'foundation_public'
        db_table = 'biz_domains'
        verbose_name = 'Domain'
        verbose_name_plural = 'Domains'

    pass
