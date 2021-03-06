from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.authtoken.models import Token
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from tenant_intake.decorators import tenant_intake_required
from tenant_reception.decorators import tenant_reception_required
from foundation_tenant.decorators import tenant_required
from foundation_tenant.models.base.communitypost import CommunityPost
from foundation_tenant.models.base.communityadvertisement import CommunityAdvertisement
from foundation_tenant.models.base.tag import Tag


@login_required(login_url='/en/login')
@tenant_required
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def community_page(request):
    """List of all the community posts in a paginated mannor."""
    filter_tag_id = request.GET.get('tag')
    posts_list = CommunityPost.objects.all() if filter_tag_id == None else CommunityPost.objects.filter(tags__id=filter_tag_id)
    paginator = Paginator(posts_list, 25) # Show 25 contacts per page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'tenant_community/list/view.html',{
        'page': 'community',
        'filter_tag_id': 0 if filter_tag_id == None else int(filter_tag_id),
        'posts': posts,
        'ads': CommunityAdvertisement.objects.all(),
        'tags': Tag.objects.all(),
    })


@login_required(login_url='/en/login')
@tenant_required
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def community_search_page(request):
    return render(request, 'tenant_community/search/view.html',{
        'page': 'community',
        'keyword': request.GET.get('keyword'),
        'tags': Tag.objects.all(),
    })
