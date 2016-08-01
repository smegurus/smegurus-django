from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.authtoken.models import Token
from foundation_config.decorators import foundation_config_required
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.models.communitypost import CommunityPost
from foundation_tenant.models.tag import Tag


@login_required(login_url='/en/login')
@foundation_config_required
@tenant_profile_required
def community_page(request):
    """List of all the community posts in a paginated mannor."""
    posts_list = CommunityPost.objects.all()
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

    return render(request, 'tenant_community/view.html',{
        'page': 'community',
        'posts': posts,
        'tags': Tag.objects.all(),
    })
