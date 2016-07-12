from django.utils.translation import ugettext_lazy as _

HOW_DISCOVERED_OPTIONS = (
    ("Google search", _("Google search")),
    ("SMEgurus.com", _("SMEgurus.com")),
    ("Social media", _("Social media")),
    ("Other", _("Other")),
)

HOW_MANY_SERVED_OPTIONS = (
    (1, _('1-10')),
    (2, _('11-50')),
    (3, _('50+')),
)

QUESTION_CATEGORY_OPTIONS = (
    (1, _('Pre-Intake Registration')),
    (2, _('Intake Registration')),
    #(3, _('All-or-None')),
)

QUESTION_TYPE_OPTIONS = (
    (1, _('Open Question')),
    (2, _('Open Closed Question - Value')),
    (2, _('Open Closed Question - Radio')),
    (2, _('Open Closed Question - Checkbox')),
    (2, _('Closed Question - Value')),
    (2, _('Closed Question - Radio')),
    (2, _('Closed Question - Checkbox')),
)

# Constants assign identification to groups.
ENTREPRENEUR_GROUP_ID = 1
MENTOR_GROUP_ID = 2
ADVISOR_GROUP_ID = 3
ORGANIZATION_MANAGER_GROUP_ID = 4
ORGANIZATION_ADMIN_GROUP_ID = 5
CLIENT_MANAGER_GROUP_ID = 6
SYSTEM_ADMIN_GROUP_ID = 7

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

TRADITIONAL_LEARNING_PREFERENCE = 1
BLENDED_LEARNING_PREFERENCE = 2
LEARNING_PREFERENCE_OPTIONS = (
    (TRADITIONAL_LEARNING_PREFERENCE, _('Traditional Learning Preference')),
    (BLENDED_LEARNING_PREFERENCE, _('Blended Learning Preference')),
)


TRADITIONAL_CHALLENGE = 1
REAL_WORLD_CHALLENGE = 2
CHALLENGE_OPTIONS = (
    (TRADITIONAL_CHALLENGE, _('Traditional Challenge')),
    (REAL_WORLD_CHALLENGE, _('Real World Challenge')),
)
