from django.db import models
from django.utils.translation import ugettext_lazy as _
from api_tenant.models.foundation.abstract_thing import AbstractThing
from api_tenant.models.foundation.postaladdress import PostalAddress
from api_tenant.models.foundation.place import Place
from api_tenant.models.foundation.contactpoint import ContactPoint
from api_tenant.models.foundation.country import Country
from api_tenant.models.foundation.brand import Brand




from foundation_tenant.models.imageupload import TenantImageUpload
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint
from foundation_tenant.models.country import Country


class AbstractPerson(AbstractThing):
    """
    A person (alive, dead, undead, or fictional).

    https://schema.org/Person
    """
    class Meta:
        abstract = True

    additional_name = models.CharField(
        _("Additional Name"),
        max_length=127,
        help_text=_('An additional name for a Person, can be used for a middle name.'),
        blank=True,
        null=True,
    )
    address = models.ForeignKey(
        PostalAddress,
        help_text=_('Physical address of the item.'),
        null=True,
        blank=True,
        related_name="abstract_person_address_%(app_label)s_%(class)s_related"
    )
    #affiliation - Organization - An organization that this person is affiliated with. For example, a school/university, a club, or a team.
    #alumniOf
    #award - text - An award won by or for this item. Supersedes awards.
    birth_date = models.DateField(
        _("birthDate"),
        help_text=_('Date of birth.'),
        blank=True,
        null=True
    )
    birth_place = models.ForeignKey(
        Place,
        help_text=_('The place where the person was born.'),
        null=True,
        blank=True,
        related_name="abstract_person_birth_place_%(app_label)s_%(class)s_related"
    )
    brand = models.ForeignKey(
        Brand,
        help_text=_('The brand(s) associated with a product or service, or the brand(s) maintained by an organization or business person.'),
        null=True,
        blank=True,
        related_name="abstract_person_organization_brand_%(app_label)s_%(class)s_related"
    )
    children = models.ManyToManyField(
        'self',
        help_text=_('A child of the person. Supersedes colleagues.'),
        blank=True,
        related_name="abstract_person_children_%(app_label)s_%(class)s_related"
    )
    colleagues = models.ManyToManyField(
        'self',
        help_text=_('A colleague of the person. Supersedes colleagues.'),
        blank=True,
        related_name="abstract_person_colleagues_%(app_label)s_%(class)s_related"
    )
    contact_point = models.ForeignKey(
        ContactPoint,
        help_text=_('A contact point for a person or organization'),
        null=True,
        blank=True,
        related_name="abstract_person_contact_point_%(app_label)s_%(class)s_related"
    )
    death_date = models.DateField(
        _("Death Date"),
        help_text=_('Date of death.'),
        blank=True,
        null=True
    )
    death_place = models.ForeignKey(
        Place,
        help_text=_('The place where the person died.'),
        null=True,
        blank=True,
        related_name="abstract_person_death_place_%(app_label)s_%(class)s_related"
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
    family_name = models.CharField(
        _("Family Name"),
        max_length=127,
        help_text=_('Family name. In the U.S., the last name of an Person. This can be used along with givenName instead of the name property.'),
        blank=True,
        null=True,
    )
    fax_number = models.CharField(
        _("Fax Number"),
        max_length=31,
        help_text=_('The fax number.'),
        blank=True,
        null=True,
    )
    follows = models.ManyToManyField(
        'self',
        help_text=_('The most generic uni-directional social relation.'),
        blank=True,
        related_name="abstract_person_follows_%(app_label)s_%(class)s_related"
    )
    gender = models.CharField(
        _("Gender"),
        max_length=31,
        help_text=_('Gender of the person.'),
        blank=True,
        null=True,
    )
    given_name = models.CharField(
        _("Given Name"),
        max_length=127,
        help_text=_('Given name. In the U.S., the first name of a Person. This can be used along with familyName instead of the name property.'),
        blank=True,
        null=True,
    )
    global_location_number = models.CharField(
        _("Global Location Number"),
        max_length=255,
        help_text=_('The <a href="http://www.gs1.org/gln">Global Location Number</a> (GLN, sometimes also referred to as International Location Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit number used to identify parties and physical locations.'),
        blank=True,
        null=True,
    )
    # hasOfferCatalog	OfferCatalog 	Indicates an OfferCatalog listing for this Organization, Person, or Service.
    # hasPOS	Place 	Points-of-Sales operated by the organization or person.
    # height	QuantitativeValue  or
    # Distance 	The height of the item.
    home_location = models.ForeignKey(
        ContactPoint,
        help_text=_('A contact location for a person\'s residence.'),
        null=True,
        blank=True,
        related_name="abstract_person_death_place_%(app_label)s_%(class)s_related"
    )
    honorific_prefix = models.CharField(
        _("Honorific Prefix"),
        max_length=5,
        help_text=_('An honorific prefix preceding a Person\'s name such as Dr/Mrs/Mr.'),
        blank=True,
        null=True,
    )
    honorific_suffix = models.CharField(
        _("Honorific Suffix"),
        max_length=5,
        help_text=_('An honorific suffix preceding a Person\'s name such as M.D. /PhD/MSCSW.'),
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
    job_title = models.CharField(
        _("Job Title"),
        max_length=127,
        help_text=_('The job title of the person (for example, Financial Manager).'),
        blank=True,
        null=True,
    )
    knows = models.ManyToManyField(
        'self',
        help_text=_('The most generic bi-directional social/work relation.'),
        blank=True,
        related_name="abstract_person_knows_%(app_label)s_%(class)s_related"
    )
    # makesOffer	Offer 	A pointer to products or services offered by the organization or person.
    # Inverse property: offeredBy.
    # memberOf	ProgramMembership or Organization 	An Organization (or ProgramMembership) to which this Person or Organization belongs.
    # Inverse property: member.
    naics = models.CharField(
        _("NAICS"),
        max_length=127,
        help_text=_('The North American Industry Classification System (NAICS) code for a particular organization or business person.'),
        blank=True,
        null=True,
    )
    nationality = models.ForeignKey(
        Country,
        help_text=_('Nationality of the person.'),
        null=True,
        blank=True,
        related_name="abstract_person_nationality_place_%(app_label)s_%(class)s_related"
    )
    # netWorth	PriceSpecification 	The total financial value of the person as calculated by subtracting assets from liabilities.
    # owns - Product or OwnershipInfo - Products owned by the organization or person.
    parents = models.ManyToManyField(
        'self',
        help_text=_('A parent of this person. Supersedes parents'),
        blank=True,
        related_name="abstract_person_parents_%(app_label)s_%(class)s_related"
    )
    # performerIn	Event 	Event that this person is a performer or participant in.
    related_to = models.ManyToManyField(
        'self',
        help_text=_('The most generic familial relation.'),
        blank=True,
        related_name="person_related_to_%(app_label)s_%(class)s_related"
    )
    # seeks	Demand 	A pointer to products or services sought by the organization or person (demand).
    siblings = models.ManyToManyField(
        'self',
        help_text=_('A sibling of the person. Supersedes siblings.'),
        blank=True,
        related_name="abstract_person_siblings_%(app_label)s_%(class)s_related"
    )
    spouse = models.ForeignKey(
        'self',
        help_text=_('The person\'s spouse.'),
        null=True,
        blank=True,
        related_name="abstract_person_nationality_place_%(app_label)s_%(class)s_related"
    )
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
    # weight	QuantitativeValue 	The weight of the product or person.
    work_location = models.ForeignKey(
        ContactPoint,
        help_text=_('A contact location for a person\'s place of work.'),
        null=True,
        blank=True,
        related_name="abstract_person_work_location_%(app_label)s_%(class)s_related"
    )
    # worksFor	Organization 	Organizations that the person works for.
