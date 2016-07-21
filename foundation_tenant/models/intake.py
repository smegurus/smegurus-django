from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.tag import Tag
from foundation_tenant import constants


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
    owner = models.OneToOneField(
        User,
        help_text=_('The User that this Intake belongs to.'),
        on_delete=models.CASCADE,
    )
    is_completed = models.BooleanField(
        _("Is completed"),
        help_text=_('Indicates if the User completed Intake.'),
        default=False,
        blank=True,
    )

    # "How Can We Help You" Section
    how_can_we_help = models.PositiveSmallIntegerField(
        _("How can we help you"),
        choices=constants.HOW_CAN_WE_HELP_OPTIONS,
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
        null=True
    )

    # "How Did You Hear About Us" Section
    how_did_you_hear = models.PositiveSmallIntegerField(
        _("How did you hear about our services"),
        choices=constants.HOW_DID_YOU_HEAR_OPTIONS,
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
        choices=constants.DO_YOU_OWN_A_BIZ_OPTIONS,
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
        choices=constants.HOW_TO_CONTACT_OPTIONS,
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
        choices=constants.HOW_TO_CONTACT_TELEPHONE_TIMES_OPTIONS,
        help_text=_('User best times to be contacted by.'),
        default=1,
    )

    def __str__(self):
        return str(self.owner.email)
