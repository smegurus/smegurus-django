# -*- coding: utf-8 -*-
from django import template
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from foundation_tenant.utils import int_or_none
from foundation_tenant.models.base.naicsoption import NAICSOption
from foundation_tenant.models.base.imageupload import TenantImageUpload
from foundation_tenant.models.bizmula.question import Question
from foundation_tenant.models.bizmula.questionanswer import QuestionAnswer
from smegurus import constants


register = template.Library()


@register.inclusion_tag('templatetags/question/template_046.html')
def render_question_type_046(workspace, module, node, question, answer):
    """
    Dependency:
    - Q99 | Total Sales Volume
    - Q100
    """
    # For this particular document and module, find the previous questions.
    q1_qid = int_or_none(question.dependency['q1_qid'])
    q2_qid = int_or_none(question.dependency['q2_qid'])
    expenses = get_object_or_404(QuestionAnswer, question_id=q1_qid)
    expenses = expenses.content
    volumes = get_object_or_404(QuestionAnswer, question_id=q2_qid)
    volumes = volumes.content

    autogen = {
        # MONTH 1
        'materials_m_1': expenses['m1'] * volumes['materials_yr1'],
        'labour_m_1': expenses['m1'] * volumes['labour_yr1'],
        'overhead_m_1': expenses['m1'] * volumes['overhead_yr1'],
        'total_m_1': expenses['m1'] * volumes['materials_yr1'] + expenses['m1'] * volumes['labour_yr1'] + expenses['m1'] * volumes['overhead_yr1'],

        # MONTH 2
        'materials_m_2': expenses['m2'] * volumes['materials_yr1'],
        'labour_m_2': expenses['m2'] * volumes['labour_yr1'],
        'overhead_m_2': expenses['m2'] * volumes['overhead_yr1'],
        'total_m_2': expenses['m2'] * volumes['materials_yr1'] + expenses['m2'] * volumes['labour_yr1'] + expenses['m2'] * volumes['overhead_yr1'],

        # MONTH 3
        'materials_m_3': expenses['m3'] * volumes['materials_yr1'],
        'labour_m_3': expenses['m3'] * volumes['labour_yr1'],
        'overhead_m_3': expenses['m3'] * volumes['overhead_yr1'],
        'total_m_3': expenses['m3'] * volumes['materials_yr1'] + expenses['m3'] * volumes['labour_yr1'] + expenses['m3'] * volumes['overhead_yr1'],

        # MONTH 4
        'materials_m_4': expenses['m4'] * volumes['materials_yr1'],
        'labour_m_4': expenses['m4'] * volumes['labour_yr1'],
        'overhead_m_4': expenses['m4'] * volumes['overhead_yr1'],
        'total_m_4': expenses['m4'] * volumes['materials_yr1'] + expenses['m4'] * volumes['labour_yr1'] + expenses['m4'] * volumes['overhead_yr1'],

        # MONTH 5
        'materials_m_5': expenses['m5'] * volumes['materials_yr1'],
        'labour_m_5': expenses['m5'] * volumes['labour_yr1'],
        'overhead_m_5': expenses['m5'] * volumes['overhead_yr1'],
        'total_m_5': expenses['m5'] * volumes['materials_yr1'] + expenses['m5'] * volumes['labour_yr1'] + expenses['m5'] * volumes['overhead_yr1'],

        # MONTH 6
        'materials_m_6': expenses['m6'] * volumes['materials_yr1'],
        'labour_m_6': expenses['m6'] * volumes['labour_yr1'],
        'overhead_m_6': expenses['m6'] * volumes['overhead_yr1'],
        'total_m_6': expenses['m6'] * volumes['materials_yr1'] + expenses['m6'] * volumes['labour_yr1'] + expenses['m6'] * volumes['overhead_yr1'],

        # MONTH 7
        'materials_m_7': expenses['m7'] * volumes['materials_yr1'],
        'labour_m_7': expenses['m7'] * volumes['labour_yr1'],
        'overhead_m_7': expenses['m7'] * volumes['overhead_yr1'],
        'total_m_7': expenses['m7'] * volumes['materials_yr1'] + expenses['m7'] * volumes['labour_yr1'] + expenses['m7'] * volumes['overhead_yr1'],

        # MONTH 8
        'materials_m_8': expenses['m8'] * volumes['materials_yr1'],
        'labour_m_8': expenses['m8'] * volumes['labour_yr1'],
        'overhead_m_8': expenses['m8'] * volumes['overhead_yr1'],
        'total_m_8': expenses['m8'] * volumes['materials_yr1'] + expenses['m8'] * volumes['labour_yr1'] + expenses['m8'] * volumes['overhead_yr1'],

        # MONTH 9
        'materials_m_9': expenses['m9'] * volumes['materials_yr1'],
        'labour_m_9': expenses['m9'] * volumes['labour_yr1'],
        'overhead_m_9': expenses['m9'] * volumes['overhead_yr1'],
        'total_m_9': expenses['m9'] * volumes['materials_yr1'] + expenses['m9'] * volumes['labour_yr1'] + expenses['m9'] * volumes['overhead_yr1'],

        # MONTH 10
        'materials_m_10': expenses['m10'] * volumes['materials_yr1'],
        'labour_m_10': expenses['m10'] * volumes['labour_yr1'],
        'overhead_m_10': expenses['m10'] * volumes['overhead_yr1'],
        'total_m_10': expenses['m10'] * volumes['materials_yr1'] + expenses['m10'] * volumes['labour_yr1'] + expenses['m10'] * volumes['overhead_yr1'],

        # MONTH 11
        'materials_m_11': expenses['m11'] * volumes['materials_yr1'],
        'labour_m_11': expenses['m11'] * volumes['labour_yr1'],
        'overhead_m_11': expenses['m11'] * volumes['overhead_yr1'],
        'total_m_11': expenses['m11'] * volumes['materials_yr1'] + expenses['m11'] * volumes['labour_yr1'] + expenses['m11'] * volumes['overhead_yr1'],

        # MONTH 12
        'materials_m_12': expenses['m12'] * volumes['materials_yr1'],
        'labour_m_12': expenses['m12'] * volumes['labour_yr1'],
        'overhead_m_12': expenses['m12'] * volumes['overhead_yr1'],
        'total_m_12': expenses['m12'] * volumes['materials_yr1'] + expenses['m12'] * volumes['labour_yr1'] + expenses['m12'] * volumes['overhead_yr1'],

        # MONTH 13
        'materials_m_13': expenses['m13'] * volumes['materials_yr2'],
        'labour_m_13': expenses['m13'] * volumes['labour_yr2'],
        'overhead_m_13': expenses['m13'] * volumes['overhead_yr2'],
        'total_m_13': expenses['m13'] * volumes['materials_yr2'] + expenses['m13'] * volumes['labour_yr2'] + expenses['m13'] * volumes['overhead_yr2'],

        # MONTH 14
        'materials_m_14': expenses['m14'] * volumes['materials_yr2'],
        'labour_m_14': expenses['m14'] * volumes['labour_yr2'],
        'overhead_m_14': expenses['m14'] * volumes['overhead_yr2'],
        'total_m_14': expenses['m14'] * volumes['materials_yr2'] + expenses['m14'] * volumes['labour_yr2'] + expenses['m14'] * volumes['overhead_yr2'],

        # MONTH 15
        'materials_m_15': expenses['m15'] * volumes['materials_yr2'],
        'labour_m_15': expenses['m15'] * volumes['labour_yr2'],
        'overhead_m_15': expenses['m15'] * volumes['overhead_yr2'],
        'total_m_15': expenses['m15'] * volumes['materials_yr2'] + expenses['m15'] * volumes['labour_yr2'] + expenses['m15'] * volumes['overhead_yr2'],

        # MONTH 16
        'materials_m_16': expenses['m16'] * volumes['materials_yr2'],
        'labour_m_16': expenses['m16'] * volumes['labour_yr2'],
        'overhead_m_16': expenses['m16'] * volumes['overhead_yr2'],
        'total_m_16': expenses['m16'] * volumes['materials_yr2'] + expenses['m16'] * volumes['labour_yr2'] + expenses['m16'] * volumes['overhead_yr2'],

        # MONTH 17
        'materials_m_17': expenses['m17'] * volumes['materials_yr2'],
        'labour_m_17': expenses['m17'] * volumes['labour_yr2'],
        'overhead_m_17': expenses['m17'] * volumes['overhead_yr2'],
        'total_m_17': expenses['m17'] * volumes['materials_yr2'] + expenses['m17'] * volumes['labour_yr2'] + expenses['m17'] * volumes['overhead_yr2'],

        # MONTH 18
        'materials_m_18': expenses['m18'] * volumes['materials_yr2'],
        'labour_m_18': expenses['m18'] * volumes['labour_yr2'],
        'overhead_m_18': expenses['m18'] * volumes['overhead_yr2'],
        'total_m_18': expenses['m18'] * volumes['materials_yr2'] + expenses['m18'] * volumes['labour_yr2'] + expenses['m18'] * volumes['overhead_yr2'],

        # MONTH 19
        'materials_m_19': expenses['m19'] * volumes['materials_yr2'],
        'labour_m_19': expenses['m19'] * volumes['labour_yr2'],
        'overhead_m_19': expenses['m19'] * volumes['overhead_yr2'],
        'total_m_19': expenses['m19'] * volumes['materials_yr2'] + expenses['m19'] * volumes['labour_yr2'] + expenses['m19'] * volumes['overhead_yr2'],

        # MONTH 20
        'materials_m_20': expenses['m20'] * volumes['materials_yr2'],
        'labour_m_20': expenses['m20'] * volumes['labour_yr2'],
        'overhead_m_20': expenses['m20'] * volumes['overhead_yr2'],
        'total_m_20': expenses['m20'] * volumes['materials_yr2'] + expenses['m20'] * volumes['labour_yr2'] + expenses['m20'] * volumes['overhead_yr2'],

        # MONTH 21
        'materials_m_21': expenses['m21'] * volumes['materials_yr2'],
        'labour_m_21': expenses['m21'] * volumes['labour_yr2'],
        'overhead_m_21': expenses['m21'] * volumes['overhead_yr2'],
        'total_m_21': expenses['m21'] * volumes['materials_yr2'] + expenses['m21'] * volumes['labour_yr2'] + expenses['m21'] * volumes['overhead_yr2'],

        # MONTH 22
        'materials_m_22': expenses['m22'] * volumes['materials_yr2'],
        'labour_m_22': expenses['m22'] * volumes['labour_yr2'],
        'overhead_m_22': expenses['m22'] * volumes['overhead_yr2'],
        'total_m_22': expenses['m22'] * volumes['materials_yr2'] + expenses['m22'] * volumes['labour_yr2'] + expenses['m22'] * volumes['overhead_yr2'],

        # MONTH 23
        'materials_m_23': expenses['m23'] * volumes['materials_yr2'],
        'labour_m_23': expenses['m23'] * volumes['labour_yr2'],
        'overhead_m_23': expenses['m23'] * volumes['overhead_yr2'],
        'total_m_23': expenses['m23'] * volumes['materials_yr2'] + expenses['m23'] * volumes['labour_yr2'] + expenses['m23'] * volumes['overhead_yr2'],

        # MONTH 24
        'materials_m_24': expenses['m24'] * volumes['materials_yr2'],
        'labour_m_24': expenses['m24'] * volumes['labour_yr2'],
        'overhead_m_24': expenses['m24'] * volumes['overhead_yr2'],
        'total_m_24': expenses['m24'] * volumes['materials_yr2'] + expenses['m24'] * volumes['labour_yr2'] + expenses['m24'] * volumes['overhead_yr2'],

        # MONTH 25
        'materials_m_25': expenses['m25'] * volumes['materials_yr3'],
        'labour_m_25': expenses['m25'] * volumes['labour_yr3'],
        'overhead_m_25': expenses['m25'] * volumes['overhead_yr3'],
        'total_m_25': expenses['m25'] * volumes['materials_yr3'] + expenses['m25'] * volumes['labour_yr3'] + expenses['m25'] * volumes['overhead_yr3'],

        # MONTH 26
        'materials_m_26': expenses['m26'] * volumes['materials_yr3'],
        'labour_m_26': expenses['m26'] * volumes['labour_yr3'],
        'overhead_m_26': expenses['m26'] * volumes['overhead_yr3'],
        'total_m_26': expenses['m26'] * volumes['materials_yr3'] + expenses['m26'] * volumes['labour_yr3'] + expenses['m26'] * volumes['overhead_yr3'],

        # MONTH 27
        'materials_m_27': expenses['m27'] * volumes['materials_yr3'],
        'labour_m_27': expenses['m27'] * volumes['labour_yr3'],
        'overhead_m_27': expenses['m27'] * volumes['overhead_yr3'],
        'total_m_27': expenses['m27'] * volumes['materials_yr3'] + expenses['m27'] * volumes['labour_yr3'] + expenses['m27'] * volumes['overhead_yr3'],

        # MONTH 28
        'materials_m_28': expenses['m28'] * volumes['materials_yr3'],
        'labour_m_28': expenses['m28'] * volumes['labour_yr3'],
        'overhead_m_28': expenses['m28'] * volumes['overhead_yr3'],
        'total_m_28': expenses['m28'] * volumes['materials_yr3'] + expenses['m28'] * volumes['labour_yr3'] + expenses['m28'] * volumes['overhead_yr3'],

        # MONTH 29
        'materials_m_29': expenses['m29'] * volumes['materials_yr3'],
        'labour_m_29': expenses['m29'] * volumes['labour_yr3'],
        'overhead_m_29': expenses['m29'] * volumes['overhead_yr3'],
        'total_m_29': expenses['m29'] * volumes['materials_yr3'] + expenses['m29'] * volumes['labour_yr3'] + expenses['m29'] * volumes['overhead_yr3'],

        # MONTH 30
        'materials_m_30': expenses['m30'] * volumes['materials_yr3'],
        'labour_m_30': expenses['m30'] * volumes['labour_yr3'],
        'overhead_m_30': expenses['m30'] * volumes['overhead_yr3'],
        'total_m_30': expenses['m30'] * volumes['materials_yr3'] + expenses['m30'] * volumes['labour_yr3'] + expenses['m30'] * volumes['overhead_yr3'],

        # MONTH 31
        'materials_m_31': expenses['m31'] * volumes['materials_yr3'],
        'labour_m_31': expenses['m31'] * volumes['labour_yr3'],
        'overhead_m_31': expenses['m31'] * volumes['overhead_yr3'],
        'total_m_31': expenses['m31'] * volumes['materials_yr3'] + expenses['m31'] * volumes['labour_yr3'] + expenses['m31'] * volumes['overhead_yr3'],

        # MONTH 32
        'materials_m_32': expenses['m32'] * volumes['materials_yr3'],
        'labour_m_32': expenses['m32'] * volumes['labour_yr3'],
        'overhead_m_32': expenses['m32'] * volumes['overhead_yr3'],
        'total_m_32': expenses['m32'] * volumes['materials_yr3'] + expenses['m32'] * volumes['labour_yr3'] + expenses['m32'] * volumes['overhead_yr3'],

        # MONTH 33
        'materials_m_33': expenses['m33'] * volumes['materials_yr3'],
        'labour_m_33': expenses['m33'] * volumes['labour_yr3'],
        'overhead_m_33': expenses['m33'] * volumes['overhead_yr3'],
        'total_m_33': expenses['m33'] * volumes['materials_yr3'] + expenses['m33'] * volumes['labour_yr3'] + expenses['m33'] * volumes['overhead_yr3'],

        # MONTH 34
        'materials_m_34': expenses['m34'] * volumes['materials_yr3'],
        'labour_m_34': expenses['m34'] * volumes['labour_yr3'],
        'overhead_m_34': expenses['m34'] * volumes['overhead_yr3'],
        'total_m_34': expenses['m34'] * volumes['materials_yr3'] + expenses['m34'] * volumes['labour_yr3'] + expenses['m34'] * volumes['overhead_yr3'],

        # MONTH 35
        'materials_m_35': expenses['m35'] * volumes['materials_yr3'],
        'labour_m_35': expenses['m35'] * volumes['labour_yr3'],
        'overhead_m_35': expenses['m35'] * volumes['overhead_yr3'],
        'total_m_35': expenses['m35'] * volumes['materials_yr3'] + expenses['m35'] * volumes['labour_yr3'] + expenses['m35'] * volumes['overhead_yr3'],

        # MONTH 36
        'materials_m_36': expenses['m36'] * volumes['materials_yr3'],
        'labour_m_36': expenses['m36'] * volumes['labour_yr3'],
        'overhead_m_36': expenses['m36'] * volumes['overhead_yr3'],
        'total_m_36': expenses['m36'] * volumes['materials_yr3'] + expenses['m36'] * volumes['labour_yr3'] + expenses['m36'] * volumes['overhead_yr3'],
    }

    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'expenses': expenses,
        'volumes': volumes,
        'autogen': autogen
    }
