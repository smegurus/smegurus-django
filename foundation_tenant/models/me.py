from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from smegurus import constants
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.abstract_person import AbstractPerson


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
        db_table = 'biz_tenant_mes'
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

    is_tos_signed = models.BooleanField(
        _("Is terms of service signed"),
        default=True, # Assume user agrees through forced Javascript code.
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

    def __str__(self):
        return str(self.id)
