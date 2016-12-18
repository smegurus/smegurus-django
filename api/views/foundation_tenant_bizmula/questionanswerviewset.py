import json
import django_filters
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.serializers.foundation_tenant_bizmula import QuestionAnswerSerializer
from foundation_tenant.models.bizmula.questionanswer import QuestionAnswer
from foundation_tenant.models.bizmula.document import Document
from foundation_tenant.models.bizmula.documenttype import DocumentType


class QuestionAnswerFilter(django_filters.FilterSet):
    class Meta:
        model = QuestionAnswer
        fields = ['workspace', 'document', 'question',]


class QuestionAnswerViewSet(viewsets.ModelViewSet):
    queryset = QuestionAnswer.objects.all()
    serializer_class = QuestionAnswerSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = QuestionAnswerFilter

    # def perform_create(self, serializer):
    #     """Add owner to the object when being created for the first time"""
    #     # Include the owner attribute directly, rather than from request data.
    #     workspace = serializer.save()
    #     workspace.owners.add(self.request.user)
    #     workspace.save()
    #
    # def perform_update(self, serializer):
    #     """Override the update function to include converting the answer string into JSON."""
    #     # Update our model.
    #     answer = serializer.save()
    #
    #     # Save data as json.
    #     answer.content = json.loads(answer.content)
    #     answer.save()
