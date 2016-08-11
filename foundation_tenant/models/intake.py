from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.me import TenantMe
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


HOW_TO_CONTACT_OPTIONS = (
    (1, _('Email')),
    (2, _('Phone')),
)


HOW_TO_CONTACT_TELEPHONE_TIMES_OPTIONS = (
    (1, _('Morning')),
    (2, _('Afternoon')),
    (3, _('Evening')),
)


class IntakeManager(models.Manager):
    def delete_all(self):
        items = Intake.objects.all()
        for item in items.all():
            item.delete()


class Intake(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_intakes'
        verbose_name = 'Intake'
        verbose_name_plural = 'Intakes'

    objects = IntakeManager()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    me = models.OneToOneField(
        TenantMe,
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
    comment = models.TextField(                   # CONTROLLED BY EMPLOYEES ONLY
        _("Comment"),
        help_text=_('A comment of this applicaitn.'),
        blank=True,
        null=True,
        default='',
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
    how_to_contact = models.PositiveSmallIntegerField(
        _("How should we contact you"),
        choices=HOW_TO_CONTACT_OPTIONS,
        help_text=_('User enters how they wish to be contacted by.'),
        default=1,
    )
    how_to_contact_telephone = models.CharField(
        _("Telephone"),
        max_length=255,
        help_text=_('The text field for telephone number.'),
        blank=True,
        null=True,
        default='',
    )
    how_to_contact_times = models.PositiveSmallIntegerField(
        _("When is it best to call you"),
        choices=HOW_TO_CONTACT_TELEPHONE_TIMES_OPTIONS,
        help_text=_('User best times to be contacted by.'),
        default=1,
    )

    def __str__(self):
        return str(self.me.name)
