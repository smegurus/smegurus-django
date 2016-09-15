from django.utils.translation import ugettext_lazy as _


# Constants assign identification to groups.
ENTREPRENEUR_GROUP_ID = 1
MENTOR_GROUP_ID = 2
ADVISOR_GROUP_ID = 3
ORGANIZATION_MANAGER_GROUP_ID = 4
ORGANIZATION_ADMIN_GROUP_ID = 5
CLIENT_MANAGER_GROUP_ID = 6
SYSTEM_ADMIN_GROUP_ID = 7


# The official name of our specific group membership.
ENTREPRENEUR_GROUP = _("Entrepreneur")
MENTOR_GROUP = _("Mentor")
ADVISOR_GROUP = _("Advisor")
ORGANIZATION_MANAGER_GROUP = _("Organization Manager")
ORGANIZATION_ADMIN_GROUP = _("Organization Administrator")
CLIENT_MANAGER_GROUP = _("Client Manager")
SYSTEM_ADMIN_GROUP = _("System Administrator")


# Constant lists all the roles belonging to the employee system of the
# application.
EMPLOYEE_GROUPS = [
    ADVISOR_GROUP,
    ORGANIZATION_MANAGER_GROUP,
    ORGANIZATION_ADMIN_GROUP,
    CLIENT_MANAGER_GROUP,
    SYSTEM_ADMIN_GROUP
]

# This array of ID's is used for grouping all "employee" staff for our app.
EMPLOYEE_GROUP_IDS = [
    ADVISOR_GROUP_ID,
    ORGANIZATION_MANAGER_GROUP_ID,
    ORGANIZATION_ADMIN_GROUP_ID,
    CLIENT_MANAGER_GROUP_ID,
    SYSTEM_ADMIN_GROUP_ID
]

# This array of ID's is used for grouping all "management" staff for our app.
MANAGEMENT_EMPLOYEE_GROUP_IDS = [
    ORGANIZATION_MANAGER_GROUP_ID,
    ORGANIZATION_ADMIN_GROUP_ID,
    CLIENT_MANAGER_GROUP_ID,
    SYSTEM_ADMIN_GROUP_ID
]


# These constants are used for Employee-Customer reviewing process.
CREATED_STATUS = 1
PENDING_REVIEW_STATUS = 2
IN_REVIEW_STATUS = 3
REJECTED_STATUS = 4
APPROVED_STATUS = 5


# These constants are used for Task model.
UNASSIGNED_TASK_STATUS = 1
ASSIGNED_TASK_STATUS = 2
INCOMPLETE_TASK_STATUS = 3
COMPLETED_TASK_STATUS = 4


# Variables control the level of detail email notification the User will
# receive when interacted by the platform.
NO_EMAIL_FREQUENCY_STATUS = 0
ESSENTIAL_EMAIL_FREQUENCY_STATUS = 1
EXCESSIVE_EMAIL_FREQUENCY_STATUS = 3


TASK_STATUS_OPTIONS = (
    (UNASSIGNED_TASK_STATUS, _('Unassigned')),
    (ASSIGNED_TASK_STATUS, _('Assigned')),
    (INCOMPLETE_TASK_STATUS, _('Incomplete')),
    (COMPLETED_TASK_STATUS, _('Complete')),
)
