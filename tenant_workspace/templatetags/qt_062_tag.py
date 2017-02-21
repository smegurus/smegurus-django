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

    processed_total_sales = {}
    # YR1
    processed_total_sales['m1'] = 0 if total_sales.content['m1'] == None else total_sales.content['m1']
    processed_total_sales['m2'] = 0 if total_sales.content['m2'] == None else total_sales.content['m2']
    processed_total_sales['m3'] = 0 if total_sales.content['m3'] == None else total_sales.content['m3']
    processed_total_sales['m4'] = 0 if total_sales.content['m4'] == None else total_sales.content['m4']
    processed_total_sales['m5'] = 0 if total_sales.content['m5'] == None else total_sales.content['m5']
    processed_total_sales['m6'] = 0 if total_sales.content['m6'] == None else total_sales.content['m6']
    processed_total_sales['m7'] = 0 if total_sales.content['m7'] == None else total_sales.content['m7']
    processed_total_sales['m8'] = 0 if total_sales.content['m8'] == None else total_sales.content['m8']
    processed_total_sales['m9'] = 0 if total_sales.content['m9'] == None else total_sales.content['m9']
    processed_total_sales['m10'] = 0 if total_sales.content['m10'] == None else total_sales.content['m10']
    processed_total_sales['m11'] = 0 if total_sales.content['m11'] == None else total_sales.content['m11']
    processed_total_sales['m12'] = 0 if total_sales.content['m12'] == None else total_sales.content['m12']
    processed_total_sales['yr1_total'] = 0 if total_sales.content['yr1_total'] == None else total_sales.content['yr1_total']

    # YR2
    processed_total_sales['m13'] = 0 if total_sales.content['m13'] == None else total_sales.content['m13']
    processed_total_sales['m14'] = 0 if total_sales.content['m14'] == None else total_sales.content['m14']
    processed_total_sales['m15'] = 0 if total_sales.content['m15'] == None else total_sales.content['m15']
    processed_total_sales['m16'] = 0 if total_sales.content['m16'] == None else total_sales.content['m16']
    processed_total_sales['m17'] = 0 if total_sales.content['m17'] == None else total_sales.content['m17']
    processed_total_sales['m18'] = 0 if total_sales.content['m18'] == None else total_sales.content['m18']
    processed_total_sales['m19'] = 0 if total_sales.content['m19'] == None else total_sales.content['m19']
    processed_total_sales['m20'] = 0 if total_sales.content['m20'] == None else total_sales.content['m20']
    processed_total_sales['m21'] = 0 if total_sales.content['m21'] == None else total_sales.content['m21']
    processed_total_sales['m22'] = 0 if total_sales.content['m22'] == None else total_sales.content['m22']
    processed_total_sales['m23'] = 0 if total_sales.content['m23'] == None else total_sales.content['m23']
    processed_total_sales['m24'] = 0 if total_sales.content['m24'] == None else total_sales.content['m24']
    processed_total_sales['yr2_total'] = 0 if total_sales.content['yr2_total'] == None else total_sales.content['yr2_total']

    # YR3
    processed_total_sales['m25'] = 0 if total_sales.content['m25'] == None else total_sales.content['m25']
    processed_total_sales['m26'] = 0 if total_sales.content['m26'] == None else total_sales.content['m26']
    processed_total_sales['m27'] = 0 if total_sales.content['m27'] == None else total_sales.content['m27']
    processed_total_sales['m28'] = 0 if total_sales.content['m28'] == None else total_sales.content['m28']
    processed_total_sales['m29'] = 0 if total_sales.content['m29'] == None else total_sales.content['m29']
    processed_total_sales['m30'] = 0 if total_sales.content['m30'] == None else total_sales.content['m30']
    processed_total_sales['m31'] = 0 if total_sales.content['m31'] == None else total_sales.content['m31']
    processed_total_sales['m32'] = 0 if total_sales.content['m32'] == None else total_sales.content['m32']
    processed_total_sales['m33'] = 0 if total_sales.content['m33'] == None else total_sales.content['m33']
    processed_total_sales['m34'] = 0 if total_sales.content['m34'] == None else total_sales.content['m34']
    processed_total_sales['m35'] = 0 if total_sales.content['m35'] == None else total_sales.content['m35']
    processed_total_sales['m36'] = 0 if total_sales.content['m36'] == None else total_sales.content['m36']
    processed_total_sales['yr3_total'] = 0 if total_sales.content['yr3_total'] == None else total_sales.content['yr3_total']

    # Update sales.
    total_sales.content = processed_total_sales
    total_sales.save()

    # Calculate totals.
    content = {
    #     # YEAR 1 OF 3
        'm1': processed_total_sales['m1'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm2': processed_total_sales['m2'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm3': processed_total_sales['m3'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm4': processed_total_sales['m4'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm5': processed_total_sales['m5'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm6': processed_total_sales['m6'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm7': processed_total_sales['m7'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm8': processed_total_sales['m8'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm9': processed_total_sales['m9'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm10': processed_total_sales['m10'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm11': processed_total_sales['m11'] * sales_per_unit.content['sales_per_unit_yr1'],
        'm12': processed_total_sales['m12'] * sales_per_unit.content['sales_per_unit_yr1'],
        'yr1_total': processed_total_sales['yr1_total'] * sales_per_unit.content['sales_per_unit_yr1'],

        # YEAR 2 OF 3
        'm13': processed_total_sales['m13'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm14': processed_total_sales['m14'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm15': processed_total_sales['m15'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm16': processed_total_sales['m16'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm17': processed_total_sales['m17'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm18': processed_total_sales['m18'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm19': processed_total_sales['m19'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm20': processed_total_sales['m20'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm21': processed_total_sales['m21'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm22': processed_total_sales['m22'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm23': processed_total_sales['m23'] * sales_per_unit.content['sales_per_unit_yr2'],
        'm24': processed_total_sales['m24'] * sales_per_unit.content['sales_per_unit_yr2'],
        'yr2_total': processed_total_sales['yr2_total'] * sales_per_unit.content['sales_per_unit_yr2'],

        # YEAR 3 OF 3
        'm25': processed_total_sales['m25'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm26': processed_total_sales['m26'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm27': processed_total_sales['m27'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm28': processed_total_sales['m28'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm29': processed_total_sales['m29'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm30': processed_total_sales['m30'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm31': processed_total_sales['m31'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm32': processed_total_sales['m32'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm33': processed_total_sales['m33'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm34': processed_total_sales['m34'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm35': processed_total_sales['m35'] * sales_per_unit.content['sales_per_unit_yr3'],
        'm36': processed_total_sales['m36'] * sales_per_unit.content['sales_per_unit_yr3'],
        'yr3_total': processed_total_sales['yr3_total'] * sales_per_unit.content['sales_per_unit_yr3'],
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
