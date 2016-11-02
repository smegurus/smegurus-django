import django_filters
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import filters
from rest_framework import status
from rest_framework import response
from rest_framework.decorators import detail_route
from api.permissions import ManagementOrAuthenticatedReadOnlyPermission
from api.pagination import LargeResultsSetPagination
from api.serializers.foundation_tenant_base import FAQItemSerializer
from foundation_tenant.models.base.faqitem import FAQItem


class FAQItemFilter(django_filters.FilterSet):
    class Meta:
        model = FAQItem
        fields = ['created','last_modified',]


class FAQItemViewSet(viewsets.ModelViewSet):
    queryset = FAQItem.objects.all()
    serializer_class = FAQItemSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, ManagementOrAuthenticatedReadOnlyPermission)
    filter_class = FAQItemFilter

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated,])
    def like(self, request, pk=None):
        faq_item = self.get_object()
        faq_item.likers.add(request.user)
        faq_item.dislikers.remove(request.user)
        faq_item.save()
        return response.Response(
            data={'message': 'Item has been liked.'},
            status=status.HTTP_200_OK
        )

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated,])
    def dislike(self, request, pk=None):
        faq_item = self.get_object()
        faq_item.likers.remove(request.user)
        faq_item.dislikers.add(request.user)
        faq_item.save()
        return response.Response(
            data={'message': 'UItem has been disliked.'},
            status=status.HTTP_200_OK
        )
