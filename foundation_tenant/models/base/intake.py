from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.governmentbenefitoption import GovernmentBenefitOption
from foundation_tenant.models.base.identifyoption import IdentifyOption
from foundation_tenant.models.base.tag import Tag
from foundation_tenant.models.base.me import Me
from foundation_tenant.models.base.note import Note
from foundation_tenant.models.base.naicsoption import NAICSOption
from smegurus import constants


STATUS_OPTIONS = (
    (constants.CREATED_STATUS, _('Created')),
    (constants.PENDING_REVIEW_STATUS, _('Pending Review')),
    (constants.IN_REVIEW_STATUS, _('In Review')),
    (constants.REJECTED_STATUS, _('Rejected')),
    (constants.APPROVED_STATUS, _('Approved')),
)


HOW_CAN_WE_HELP_OPTIONS = (
    (1, _('I am interested in one of your programs')),
    (2, _('I am interested in one of your services')),
    (3, _('I want to find out how to start a business')),
    (4, _('I have an existing business I need help with')),
    (5, _('I want to find out about grants and loans')),
    (6, _('Other')),
)


HOW_DID_YOU_HEAR_OPTIONS = (
    (1, _('Google Search')),
    (2, _('Your Website')),
    (3, _('Other')),
)


DO_YOU_OWN_A_BIZ_OPTIONS = (
    (1, _('Yes')),
    (2, _('No')),
    (3, _('In the process of starting')),
    (4, _('I previously owned a business')),
    (5, _('None of the above')),
)


TELEPHONE_TIMES_OPTIONS = (
    (1, _('Morning')),
    (2, _('Afternoon')),
    (3, _('Evening')),
    (4, _('Anytime')),
)


HAS_TELEPHONE_OPTIONS = (
    (1, _('No')),
    (2, _('Yes')),
)


class IntakeManager(models.Manager):
    def delete_all(self):
        items = Intake.objects.all()
        for item in items.all():
            item.delete()


class Intake(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_intakes'
        verbose_name = 'Intake'
        verbose_name_plural = 'Intakes'

    objects = IntakeManager()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    me = models.OneToOneField(
        Me,
        help_text=_('The User that this Intake belongs to.'),
        on_delete=models.CASCADE,
    )
    status = models.PositiveSmallIntegerField(    # CONTROLLED BY EMPLOYEES ONLY
        _("Status"),
        choices=STATUS_OPTIONS,
        help_text=_('The state this intake application is in our application.'),
        default=constants.CREATED_STATUS,
        db_index=True,
    )
    is_employee_created = models.BooleanField(    # CONTROLLED BY EMPLOYEES ONLY
        _("Is Employee Created"),
        default=False,
        help_text=_('Variable controls whether the intake was created by the Advisor or not.'),
    )

    # "How Can We Help You" Section
    how_can_we_help = models.PositiveSmallIntegerField(
        _("How can we help you"),
        choices=HOW_CAN_WE_HELP_OPTIONS,
        help_text=_('The details of how we can help the User.'),
        default=1,
    )
    how_can_we_help_other = models.CharField(
        _("Other"),
        max_length=255,
        help_text=_('The text field for other.'),
        blank=True,
        null=True,
        default='',
    )
    how_can_we_help_tag = models.ForeignKey(
        Tag,
        help_text=_('The Tag the User is interested in.'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    # "How Did You Hear About Us" Section
    how_did_you_hear = models.PositiveSmallIntegerField(
        _("How did you hear about our services"),
        choices=HOW_DID_YOU_HEAR_OPTIONS,
        help_text=_('The details of how we can help the User.'),
        default=1,
    )
    how_did_you_hear_other = models.CharField(
        _("Other"),
        max_length=255,
        help_text=_('The text field for other.'),
        blank=True,
        null=True,
        default='',
    )

    # "Do You Own a Business" Section
    do_you_own_a_biz = models.PositiveSmallIntegerField(
        _("Do you currently own a business"),
        choices=DO_YOU_OWN_A_BIZ_OPTIONS,
        help_text=_('User enters their current business owning status.'),
        default=1,
    )
    do_you_own_a_biz_other = models.CharField(
        _("Other"),
        max_length=255,
        help_text=_('The text field for other.'),
        blank=True,
        null=True,
        default='',
    )

    # "How should we contact you" Section
    has_telephone = models.PositiveSmallIntegerField(
        _("Would you like to include your telephone?"),
        choices=HAS_TELEPHONE_OPTIONS,
        default=1,
        help_text=_('Would you like to include your telephone?'),
    )
    telephone = models.CharField(
        _("Telephone"),
        max_length=255,
        help_text=_('The text field for telephone number.'),
        blank=True,
        null=True,
        default='',
    )
    telephone_time = models.PositiveSmallIntegerField(
        _("When is it best to call you"),
        choices=TELEPHONE_TIMES_OPTIONS,
        help_text=_('User best times to be contacted by.'),
        default=1,
    )

    # Terms & Conditions.
    has_signed_privacy_and_terms = models.BooleanField(
        _("Has Signed Privacy Policy and Terms of Use"),
        default=False,
        help_text=_('Has User agreed to our Privacy Policy and Terms of Use policy.'),
    )
    has_signed_confidentiality_agreement = models.BooleanField(
        _("Has Signed Confidentiality Agreement"),
        default=False,
        help_text=_('Has User agreed to our Confidentiality Agreement.'),
    )
    has_signed_collection_and_use_of_information = models.BooleanField(
        _("Has Signed Confidentiality Agreement"),
        default=False,
        help_text=_('Has User agreed to our Confidentiality Agreement.'),
    )
    has_signed_with_name = models.CharField(
        _("Has Signed with Name"),
        max_length=127,
        help_text=_('The name the User has signed with.'),
        blank=True,
        null=True,
        default='',
    )
    has_signed_on_date = models.DateTimeField(
        _("Has Signed on Date"),
        help_text=_('The timestamp of when the User officially signed our agreements.'),
        blank=True,
        null=True,
    )

    # "Do you currently receive any of the following government benefits?" Section
    government_benefits = models.ManyToManyField(
        GovernmentBenefitOption,
        help_text=_('The government benefits that belong to this Intake.'),
        blank=True,
        related_name='intake_government_benefits_%(app_label)s_%(class)s_related',
    )
    other_government_benefit = models.CharField(
        _("Other Government Benefit"),
        max_length=127,
        help_text=_('The textfield used to take other benefits not mentioned in our list.'),
        blank=True,
        null=True,
        default='',
    )

    # "Do any of the following statements apply to you" Section
    identities = models.ManyToManyField(
        IdentifyOption,
        help_text=_('The identify options belong to this Intake.'),
        blank=True,
        related_name='intake_identify_%(app_label)s_%(class)s_related',
    )

    # "What is your date of birth" Section.
    date_of_birth = models.DateField(blank=True, null=True)

    # "Has business idea" Section.
    has_business_idea = models.BooleanField(    # CONTROLLED BY EMPLOYEES ONLY
        _("I have a business idea"),
        default=False,
        help_text=_('Variable controls whether the entrepreneur has a business or not.'),
    )

    # "What sector does your current business idea mainly fall into?" Section.
    naics_depth_one = models.ForeignKey(
        NAICSOption,
        help_text=_('The NAICS option for depth one.'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='intake_naics_depth_one_%(app_label)s_%(class)s_related',
    )
    naics_depth_two = models.ForeignKey(
        NAICSOption,
        help_text=_('The NAICS option for depth two.'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='intake_naics_depth_two_%(app_label)s_%(class)s_related',
    )
    naics_depth_three = models.ForeignKey(
        NAICSOption,
        help_text=_('The NAICS option for depth three.'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='intake_inaics_depth_three_%(app_label)s_%(class)s_related',
    )
    naics_depth_four = models.ForeignKey(
        NAICSOption,
        help_text=_('The NAICS option for depth four.'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='intake_naics_depth_four_%(app_label)s_%(class)s_related',
    )
    naics_depth_five = models.ForeignKey(
        NAICSOption,
        help_text=_('The NAICS option for depth five.'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='intake_naics_depth_five_%(app_label)s_%(class)s_related',
    )

    # Notes:
    judgement_note = models.ForeignKey(
        Note,
        help_text=_('The comments that where entered during the Intake judgement process.'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='intake_judgement_note_%(app_label)s_%(class)s_related',
    )
    privacy_note = models.ForeignKey(
        Note,
        help_text=_('The note indicating whether User has signed the privacy policy document or not.'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='intake_privacy_note_%(app_label)s_%(class)s_related',
    )
    terms_note = models.ForeignKey(
        Note,
        help_text=_('The note indicating whether User has signed the terms of use document or not.'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='intake_terms_note_%(app_label)s_%(class)s_related',
    )
    confidentiality_note = models.ForeignKey(
        Note,
        help_text=_('The note indicating whether User has signed the confidentiality document or not.'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='intake_confidentiality_note_%(app_label)s_%(class)s_related',
    )
    collection_note = models.ForeignKey(
        Note,
        help_text=_('The note indicating whether User has signed the collection and use of information document or not.'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='intake_collection_note_%(app_label)s_%(class)s_related',
    )

    def __str__(self):
        return str(self.me.name)
