# -*- coding: utf-8 -*-
from django import template
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from foundation_tenant.utils import int_or_none
from foundation_tenant.models.base.naicsoption import NAICSOption
from foundation_tenant.models.base.imageupload import ImageUpload
from foundation_tenant.models.bizmula.question import Question
from foundation_tenant.models.bizmula.questionanswer import QuestionAnswer
from smegurus import constants


register = template.Library()


@register.inclusion_tag('templatetags/question/template_062.html')
def render_question_type_062(workspace, module, node, question, answer):
    """
    Dependency:
    - Q99 | Total Sales Volume
    - Q100
    """
    # For this particular document and module, find the previous questions.
    q1_qid = int_or_none(question.dependency['q1_qid'])
    q2_qid = int_or_none(question.dependency['q2_qid'])
    total_sales = QuestionAnswer.objects.get(
        question_id=q1_qid,
        workspace=workspace
    )
    sales_per_unit = QuestionAnswer.objects.get(
        question_id=q2_qid,
        workspace=workspace
    )

    # DEBUGGING PURPOSES ONLY.
    # print("------|", total_sales.question.id, "|------")
    # print(total_sales.content)
    # print("\n")
    # print("------|", sales_per_unit.question.id, "|------")
    # print(sales_per_unit.content)
    # print("\n")

    # Calculate totals.
    content = {
        # YEAR 1 OF 3
        'm1': total_sales.content['m1'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm2': total_sales.content['m2'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm3': total_sales.content['m3'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm4': total_sales.content['m4'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm5': total_sales.content['m5'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm6': total_sales.content['m6'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm7': total_sales.content['m7'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm8': total_sales.content['m8'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm9': total_sales.content['m9'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm10': total_sales.content['m10'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm11': total_sales.content['m11'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm12': total_sales.content['m12'] * sales_per_unit.content['sales_per_unit_yr1'],
        'yr1_total': total_sales.content['yr1_total'] * sales_per_unit.content['sales_per_unit_yr1'],

        # YEAR 2 OF 3
        'm13': total_sales.content['m13'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm14': total_sales.content['m14'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm15': total_sales.content['m15'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm16': total_sales.content['m16'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm17': total_sales.content['m17'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm18': total_sales.content['m18'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm19': total_sales.content['m19'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm20': total_sales.content['m20'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm21': total_sales.content['m21'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm22': total_sales.content['m22'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm23': total_sales.content['m23'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm24': total_sales.content['m24'] * sales_per_unit.content['sales_per_unit_yr2'],
        'yr2_total': total_sales.content['yr2_total'] * sales_per_unit.content['sales_per_unit_yr2'],

        # YEAR 3 OF 3
        'm25': total_sales.content['m25'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm26': total_sales.content['m26'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm27': total_sales.content['m27'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm28': total_sales.content['m28'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm29': total_sales.content['m29'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm30': total_sales.content['m30'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm31': total_sales.content['m31'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm32': total_sales.content['m32'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm33': total_sales.content['m33'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm34': total_sales.content['m34'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm35': total_sales.content['m35'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm36': total_sales.content['m36'] * sales_per_unit.content['sales_per_unit_yr3'],
        'yr3_total': total_sales.content['yr3_total'] * sales_per_unit.content['sales_per_unit_yr3'],
    }

    # Save the answer content.
    answer.content = content
    answer.save()

    # Return result.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
    }
