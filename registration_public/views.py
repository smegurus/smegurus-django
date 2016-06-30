from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.translation import get_language
from django.contrib.auth.models import User


def org_owner_registration_page(request):
    return render(request, 'registration_public/register_view.html',{

    })


def org_owner_activation_required_page(request):
    return render(request, 'registration_public/activation_required_view.html',{

    })
