from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from foundation_public.decorators import group_required
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.decorators import tenant_required
from foundation_tenant.models.base.me import Me
from foundation_tenant.models.base.note import Note
from foundation_tenant.forms.noteform import NoteForm
from smegurus import constants


@login_required(login_url='/en/login')
@tenant_required
@tenant_configuration_required
@tenant_profile_required
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
def entrepreneur_master_page(request, id):
    me = get_object_or_404(Me, pk=int(id))
    notes = Note.objects.filter(me=me)
    return render(request, 'tenant_note/master/view.html',{
        'page': 'note',
        'me': me,
        'notes': notes,
    })


@login_required(login_url='/en/login')
@tenant_required
@tenant_configuration_required
@tenant_profile_required
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
def entrepreneur_details_page(request, me_id, note_id):
    me = get_object_or_404(Me, pk=int(me_id))
    note = get_object_or_404(Note, pk=int(note_id))
    return render(request, 'tenant_note/details/view.html',{
        'page': 'note',
        'me': me,
        'form': NoteForm(instance=note)
    })


@login_required(login_url='/en/login')
@tenant_required
@tenant_configuration_required
@tenant_profile_required
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
def entrepreneur_create_page(request, id):
    me = get_object_or_404(Me, pk=int(id))
    return render(request, 'tenant_note/create/view.html',{
        'page': 'note',
        'me': me,
        'form': NoteForm()
    })
