from django.utils.translation import ugettext_lazy as _

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

# Constant lists all the roles belonging to the employee system of the
# application.
EMPLOYEE_GROUPS = [
    _("Advisor"),
    _("Organization Manager"),
    _("Organization Administrator"),
    _("Client Manager"),
    _("System Administrator")
]