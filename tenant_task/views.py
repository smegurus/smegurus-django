from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.views.decorators.http import condition
from django.db.models import Q
from rest_framework.authtoken.models import Token
from tenant_intake.decorators import tenant_intake_required
from tenant_profile.decorators import tenant_profile_required
from tenant_configuration.decorators import tenant_configuration_required
from smegurus import constants
from foundation_tenant.models.me import TenantMe
from foundation_tenant.forms.tagform import TagForm
from foundation_tenant.forms.intakeform import IntakeForm
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.intake import Intake


# def latest_task_master(request):
#     try:
#         return Note.objects.latest("last_modified").last_modified
#     except Note.DoesNotExist:
#         return datetime.now()


# def latest_note_details(request, me_id, note_id):
#     try:
#         return Note.objects.filter(
#             me_id=int(me_id),
#             id=int(note_id)
#         ).latest("last_modified").last_modified
#     except Note.DoesNotExist:
#         return datetime.now()


@login_required(login_url='/en/login')
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
# @condition(last_modified_func=latest_note_master)
def tasks_list_page(request):
    return render(request, 'tenant_task/list/view.html',{
        'page': 'tasks',
    })
