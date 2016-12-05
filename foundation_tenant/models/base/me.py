from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.tag import Tag
from foundation_tenant.models.base.abstract_person import AbstractPerson
from smegurus import constants


TASK_EMAIL_FREQUENCY_OPTIONS = (
    (constants.NO_EMAIL_FREQUENCY_STATUS, _('Do not send any emails')),
    (constants.ESSENTIAL_EMAIL_FREQUENCY_STATUS, _('Send only essential emails')),
    (constants.EXCESSIVE_EMAIL_FREQUENCY_STATUS, _('Send all emails')),
)

class TenantMeManager(models.Manager):
    def get_by_owner_or_none(self, owner):
        try:
            return TenantMe.objects.get(owner=owner)
        except TenantMe.DoesNotExist:
            return None

    def delete_all(self):
        items = TenantMe.objects.all()
        for item in items.all():
            item.delete()


class TenantMe(AbstractPerson):
    """
    The object to represent the "TenantMe" object for all the tenanted objects.
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_tenant_mes'
        verbose_name = 'Tenant Me'
        verbose_name_plural = 'Tenant Mes'

    objects = TenantMeManager()
    is_admitted = models.BooleanField(  # CONTROLLED BY EMPLOYEES ONLY
        _("Is Admitted"),
        default=False,
        help_text=_('Variable controls whether the user has been accepted into our Organization for any number of programs.'),
    )
    tags = models.ManyToManyField(
        Tag,
        help_text=_('The tags that this User belongs to.'),
        blank=True,
        related_name="tenant_me_tags_%(app_label)s_%(class)s_related"
    )
    stage_num = models.PositiveSmallIntegerField(            # CONTROLLED BY SYSTEM
        _("Stage Number"),
        help_text=_('Track what stage this User is in the system (If they are an entrepreneur).'),
        default=constants.ME_MIN_STAGE_NUM,
        db_index=True,
    )
    temporary_password = models.CharField(# CONTROLLED BY SYSTEM & PRIVATE FROM API.
        _("Temporary Password"),
        max_length=8,
        help_text=_('The temporary password generated by the system.'),
        blank=True,
        null=True,
    )

    # Legal confirmation.
    is_tos_signed = models.BooleanField(
        _("Is terms of service signed"),
        default=True, # Assume user agrees through forced Javascript code.
    )

    # User metrics.
    gender = models.PositiveSmallIntegerField(
        _("Gender"),
        choices=constants.ME_GENDER_OPTIONS,
        help_text=_('The gender this User identifies as.'),
        blank=True,
        default=1,
    )
    gender_other = models.CharField(
        _("Gender Other"),
        max_length=127,
        help_text=_('Allow the user to enter a custom gender field.'),
        blank=True,
        null=True
    )
    level_of_education = models.PositiveSmallIntegerField(
        _("Highest Level of Education"),
        choices=constants.HIGHEST_LEVEL_OF_EDUCATION_OPTIONS,
        help_text=_('The highest level of education this User has attained.'),
        blank=True,
        default=1,
    )
    level_of_education_other = models.CharField(
        _("Highest Level of Education Other"),
        max_length=127,
        help_text=_('Allow the user to enter a custom highest level of education field.'),
        blank=True,
        null=True
    )
    place_of_birth = models.CharField(
        _("Place of Birth"),
        max_length=127,
        choices=constants.ME_PLACE_OF_BIRTH_OPTIONS,
        help_text=_('The place this User was born.'),
        blank=True,
        null=True
    )
    place_of_birth_other = models.CharField(
        _("Place of Birth Other"),
        max_length=127,
        help_text=_('Allow the user to enter a custom place of birth field.'),
        blank=True,
        null=True
    )
    employment_status = models.PositiveSmallIntegerField(
        _("Employment Status"),
        choices=constants.ME_EMPLOYMENT_STATUS_OPTIONS,
        help_text=_('The employment status of this User.'),
        blank=True,
        default=1,
    )
    employment_status_other = models.CharField(
        _("Employment Status"),
        max_length=127,
        help_text=_('Allow the user to enter a custom employment status field.'),
        blank=True,
        null=True
    )
    education_or_training_status = models.PositiveSmallIntegerField(
        _("Education or Training Status"),
        choices=constants.ME_IN_EDUCATION_OR_TRAINING_STATUS_OPTIONS,
        help_text=_('The employment status of this User.'),
        blank=True,
        default=1,
    )
    education_or_training_status_other = models.CharField(
        _("Education or Training Status"),
        max_length=127,
        help_text=_('Allow the user to enter a custom employment status field.'),
        blank=True,
        null=True
    )
    why_be_entrepreneur = models.PositiveSmallIntegerField(
        _("Why be an Entrepreneur"),
        choices=constants.ME_WHY_BE_ENTREPRENEUR_OPTIONS,
        help_text=_('Enter why the User wants to be an entrepreneur.'),
        blank=True,
        default=1,
    )
    why_be_entrepreneur_other = models.CharField(
        _("Why be an Entrepreneur Other"),
        max_length=127,
        help_text=_('Allow the user to enter a custom why be an entrepreneur field.'),
        blank=True,
        null=True
    )
    challenges_becoming_entrepreneur = models.PositiveSmallIntegerField(
        _("Challenges becoming Entrepreneur"),
        choices=constants.ME_CHALLENGES_BECOMING_ENTREPRENEUR_OPTIONS,
        help_text=_('Enter challenges in becoming entrepreneur.'),
        blank=True,
        default=1,
    )
    challenges_becoming_entrepreneur_other = models.CharField(
        _("Challenges becoming Entrepreneur Other"),
        max_length=127,
        help_text=_('Allow  field.'),
        blank=True,
        null=True
    )
    annual_income_bracket = models.PositiveSmallIntegerField(
        _("Annual Income Bracket"),
        choices=constants.ME_ANNUAL_INCOME_BRACKET_OPTIONS,
        help_text=_('Enter your annual income bracket.'),
        default=1,
    )
    has_owned_business = models.PositiveSmallIntegerField(
        _("Has Owned Business"),
        choices=constants.ME_HAS_OWNED_BUSINESS_OPTIONS,
        help_text=_('Enter has owned business.'),
        default=1,
    )
    has_owned_business_other = models.CharField(
        _("Has Owned Business Other"),
        max_length=127,
        help_text=_('Allow has owned business other field.'),
        blank=True,
        null=True
    )

    # Controls whether the User has to go through a Profile Setup screens
    # before being granted access to the main application (Dashboard, etc).
    is_setup = models.BooleanField(
        _("Is this account setup and ready"),
        default=False,
        help_text=_('Variable controls whether the user profile has been setup.'),
    )

    # Controls whether the screen is locked or not.
    is_locked = models.BooleanField(
        _("Is Locked"),
        default=False,
        help_text=_('Controls whether the screen is locked or not.'),
    )

    # Notification Control Variables.
    notify_when_task_had_an_interaction = models.BooleanField(
        _("Alert me when a task, that I am a participant in, had an interaction"),
        default=True
    )
    notify_when_new_messages = models.BooleanField(
        _("Alert me when I receive a new message"),
        default=True
    )
    notify_when_due_tasks = models.BooleanField(
        _("Alert me when I have an item due within 2 days"),
        default=True
    )

    has_logout_dialog = models.BooleanField(
        _("Has Logout Dialog"),
        default=True,
        help_text=_('Variable indicates whether Users are prompted with a dialog during logout.'),
    )
    managed_by = models.ForeignKey(
        'self',
        help_text=_('The Users whom manages this User.'),
        blank=True,
        null=True,
        related_name="tenant_me_managed_by_%(app_label)s_%(class)s_related",
        on_delete=models.SET_NULL
    )

    def is_entrepreneur(self):
        for my_group in self.owner.groups.all():
            if constants.ENTREPRENEUR_GROUP_ID == my_group.id:
                return True
        return False

    def is_employee(self):
        for my_group in self.owner.groups.all():
            for employee_group_id in constants.EMPLOYEE_GROUP_IDS:
                if employee_group_id == my_group.id:
                    return True
        return False

    def is_manager(self):
        for my_group in self.owner.groups.all():
            for management_group_id in constants.MANAGEMENT_EMPLOYEE_GROUP_IDS:
                if management_group_id == my_group.id:
                    return True
        return False

    def is_org_admin(self):
        for my_group in self.owner.groups.all():
            for admin_group_id in constants.ORG_ADMIN_GROUP_IDS:
                if admin_group_id == my_group.id:
                    return True
        return False

    def __str__(self):
        return str(self.id)
