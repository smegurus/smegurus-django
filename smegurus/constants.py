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
SUSPENDED_STATUS = 6
EXPIRED_STATUS = 7
STATUS_OPTIONS = (
    (CREATED_STATUS, _('Created')),
    (PENDING_REVIEW_STATUS, _('Pending')),
    (IN_REVIEW_STATUS, _('In Review')),
    (REJECTED_STATUS, _('Rejected')),
    (APPROVED_STATUS, _('Approved')),
    (SUSPENDED_STATUS, _('Suspended')),
    (EXPIRED_STATUS, _('Expired')),
)


# These constants are used for Task model.
UNASSIGNED_TASK_STATUS = 1
ASSIGNED_TASK_STATUS = 2
INCOMPLETE_TASK_STATUS = 3
COMPLETED_TASK_STATUS = 4
COMPLETED_TASK_AND_VERIFIED_STATUS = 5


# Constants control the level of detail email notification the User will
# receive when interacted by the platform.
NO_EMAIL_FREQUENCY_STATUS = 0
ESSENTIAL_EMAIL_FREQUENCY_STATUS = 1
EXCESSIVE_EMAIL_FREQUENCY_STATUS = 3
TASK_STATUS_OPTIONS = (
    (UNASSIGNED_TASK_STATUS, _('Unassigned')),
    (ASSIGNED_TASK_STATUS, _('Assigned')),
    (INCOMPLETE_TASK_STATUS, _('Incomplete')),
    (COMPLETED_TASK_STATUS, _('Complete')),
    (COMPLETED_TASK_AND_VERIFIED_STATUS, _('Complete and verified')),
)


# Constants control what type of Tasks are available in our system.
TASK_BASIC_TYPE = 1
TASK_CALENDAR_TYPE = 2
TASK_DOCGEN_TYPE = 3
TASK_LEARNING_TYPE = 4
TASK_WEBFORM_TYPE = 5
TASK_UPLOAD_TYPE = 6
TASK_RESOURCE_TYPE = 7
TASK_TYPE_OPTIONS = (
    (TASK_BASIC_TYPE, _('Basic Task')),
    (TASK_CALENDAR_TYPE, _('Calendar Task')),
    (TASK_DOCGEN_TYPE, _('Document Generation Task')),
    (TASK_LEARNING_TYPE, _('Learning Task')),
    (TASK_WEBFORM_TYPE, _('Web Form Task')),
    (TASK_UPLOAD_TYPE, _('Upload Task')),
    (TASK_RESOURCE_TYPE, _('Resource Task')),
)


# Constants used for Calendar Events.
CALENDAR_EVENT_BY_CUSTOM_TYPE = 1
CALENDAR_EVENT_BY_TAG_TYPE = 2
CALENDAR_EVENT_TYPE_OPTIONS = (
    (CALENDAR_EVENT_BY_CUSTOM_TYPE, _('Calendar Event by Custom')),
    (CALENDAR_EVENT_BY_TAG_TYPE, _('Calendar Event by Tag')),
)


# Constants used for Informational Resources.
INFO_RESOURCE_INTERAL_URL_TYPE = 1
INFO_RESOURCE_EXTERNAL_URL_TYPE = 2
INFO_RESOURCE_EMBEDDED_YOUTUBE_VIDEO_TYPE = 3
INFO_RESOURCE_EXTERNAL_YOUTUBE_VIDEO_TYPE = 4
INFO_RESOURCE_TYPE_OPTIONS = (
    (INFO_RESOURCE_INTERAL_URL_TYPE, _('Internal URL')),
    (INFO_RESOURCE_EXTERNAL_URL_TYPE, _('External URL')),
    (INFO_RESOURCE_EMBEDDED_YOUTUBE_VIDEO_TYPE, _('Embedded YouTube Video')),
    (INFO_RESOURCE_EXTERNAL_YOUTUBE_VIDEO_TYPE, _('External YouTube Video')),
)
