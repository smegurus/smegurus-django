# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from foundation_tenant.models.base.s3file import S3File


@login_required(login_url='/en/sign-in')
def s3file_timed_url(request, signed_s3_file_id, expiry_time=60):
    """
    Function will look for any AJAX calls that where made for the
    authenticated User and lookup the S3File for the 'id' and only
    return the S3File UFL if it meets our authorization requirements.
    """
    response_data = {'url' : ''}

    # Verify the S3File ID exists in our database and process permissions.
    if request.is_ajax():
        s3file = S3File.objects.get_by_verifying_pk(signed_s3_file_id)
        if s3file:
            if is_s3_file_permission_granted(s3file, request.user):
                response_data['url'] = s3file.get_absolute_url()
    return JsonResponse(response_data, safe=False)


def is_s3_file_permission_granted(s3file, user):
    return True
    # return False  # Deny access for any anomolous reasons.


def delete_s3file(request, signed_s3_file_id):
    """
    Function will look for any AJAX calls that where made for the
    authenticated User and lookup the S3File for the 'id' and only
    delete this S3File if our request meets our authorization requirements.
    """
    response_data = {}

    # Verify the S3File ID exists in our database and process permissions.
    if request.is_ajax():
        s3file = S3File.objects.get_by_verifying_pk(signed_s3_file_id)
        if s3file:
            if is_s3_file_permission_granted(s3file, request.user):
                # Delete our file since permission has been granted.
                s3file.delete()
    return JsonResponse(response_data, safe=False)
