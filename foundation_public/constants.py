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

# Constant lists all the roles belonging to the employee system of the
# application.
EMPLOYEE_GROUPS = [
    _("Advisor"),
    _("Organization Manager"),
    _("Organization Administrator"),
    _("Client Manager"),
    _("System Administrator")
]
