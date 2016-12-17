# -*- coding: utf-8 -*-
import json
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


@register.simple_tag
def reverse_previous_node(workspace, module, node):
    if node['previous_position'] == -1:
        return reverse('tenant_workspace_module_start_master', args=[workspace.id, module.id,])
    else:
        return reverse('tenant_workspace_module_detail', args=[workspace.id, module.id, node['previous_position'],])


@register.simple_tag
def reverse_next_node(workspace, module, node):
    if node['next_position'] == -1:
        return reverse('tenant_workspace_module_finish_master', args=[workspace.id, module.id, 0])
    else:
        return reverse('tenant_workspace_module_detail', args=[workspace.id, module.id, node['next_position'],])


@register.inclusion_tag('templatetags/question/template_001.html')
def render_question_type_001(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': json.loads(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_002.html')
def render_question_type_002(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': json.loads(answer.content),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_003.html')
def render_question_type_003(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_004.html')
def render_question_type_004(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked),
        "OTHER_TEXT": "other"
    }


@register.inclusion_tag('templatetags/question/template_005.html')
def render_question_type_005(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': json.loads(answer.content),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_006.html')
def render_question_type_006(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_007.html')
def render_question_type_007(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': json.loads(answer.content),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_008.html')
def render_question_type_008(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_009.html')
def render_question_type_009(workspace, module, node, question, answer):
    """
    DEPENDENCY:
    - template #001 | QID: 10 | geographic market
    """
    # For this particular document and module, find the previous question.
    previous_question_id = int_or_none(question.dependency['previous_question_id'])
    previous_question_answer = get_object_or_404(QuestionAnswer, question_id=previous_question_id)

    # Input the variables into the template and render the view.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': json.loads(answer.content),  # Convert string to JSON dictionary.
        'previous_picked': json.loads(previous_question_answer.content),  # Convert string to JSON dictionary.
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_010.html')
def render_question_type_010(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_011.html')
def render_question_type_011(workspace, module, node, question, answer):
    # Convert JSON string into python dictionary.
    picked = json.loads(answer.content)

    # Fetch the image that is associated with this question's answer.
    imageupload = None
    if bool(picked):
        upload_id = int_or_none(picked['var_1'])
        imageupload = TenantImageUpload.objects.get(id=upload_id)

    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'imageupload': imageupload,
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_012.html')
def render_question_type_012(workspace, module, node, question, answer):
    """
    DEPENDENCY:
    - NAICSOption
    """
    # Convert JSON string into python dictionary.
    picked = json.loads(answer.content)

    # If the answer was not created then we will pre-create the format.
    if not bool(picked):
        picked = {
            'var_1': '',
            'var_2': '',
            'var_3': '',
            'var_4': '',
            'var_5': '',
            'var_6': ''
        }

    # Get the first depth.
    depth_one_results = NAICSOption.objects.filter(parent=None)

    # Get the second depth.
    depth_two_results = None
    if picked['var_2']:
        depth_two_results = NAICSOption.objects.filter(parent=picked['var_1'])
    else:
        if picked['var_1']:
            depth_two_results = NAICSOption.objects.filter(parent=picked['var_1'])

    # # Get the three depth.
    depth_three_results = None
    if picked['var_3']:
        depth_three_results = NAICSOption.objects.filter(parent=picked['var_2'])
    else:
        if picked['var_2']:
            depth_three_results = NAICSOption.objects.filter(parent=picked['var_2'])

    # # Get the four depth.
    depth_four_results = None
    if picked['var_4']:
        depth_four_results = NAICSOption.objects.filter(parent=picked['var_3'])
    else:
        if picked['var_3']:
            depth_four_results = NAICSOption.objects.filter(parent=picked['var_3'])

    # # Get the five depth.
    depth_five_results = None
    if picked['var_5']:
        depth_five_results = NAICSOption.objects.filter(parent=picked['var_4'])
    else:
        if picked['var_4']:
            depth_five_results = NAICSOption.objects.filter(parent=picked['var_4'])

    # Render template.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': json.loads(answer.content),
        "OTHER_TEXT": "Other (Please Specify)",
        'depth_one_results': depth_one_results,
        'depth_two_results': depth_two_results,
        'depth_three_results': depth_three_results,
        'depth_four_results': depth_four_results,
        'depth_five_results': depth_five_results
    }


@register.inclusion_tag('templatetags/question/template_013.html')
def render_question_type_013(workspace, module, node, question, answer):
    """
    DEPENDENCY:
    - template #002 | QTYPE_ID: 61 | company name
    - template #001 | QTYPE_ID: 10 | geographic market
    - template #009 | QTYPE_ID: 11 | geographic market
    - NAICSOption
    """
    # Convert JSON string into python dictionary.
    picked = json.loads(answer.content)
    OTHER_TEXT = "Other (Please Specify)"

    # For this particular document and module, find the previous questions.
    q1_qid = int_or_none(question.dependency['q1_qid'])
    q2_qid = int_or_none(question.dependency['q2_qid'])
    q3_qid = int_or_none(question.dependency['q3_qid'])
    a1_raw = get_object_or_404(QuestionAnswer, question_id=q1_qid)
    a1 = json.loads(a1_raw.content)
    a2_raw = get_object_or_404(QuestionAnswer, question_id=q2_qid)
    a2 = json.loads(a2_raw.content)
    a3_raw = get_object_or_404(QuestionAnswer, question_id=q3_qid)
    a3 = json.loads(a3_raw.content)

    # Generate custom text from previous questions.
    # 1. Generate company name.
    company_name = a1['var_1']
    has_short_name = bool(a1['var_2'])
    if has_short_name:
        company_name = a1['var_3']

    # 2. Generate geographic info.
    company_market = a3['var_1'] if len( a3['var_1']) else a3['var_0'] # Note: Handle "Online" and "Worldwide".

    # 3. Generate text.
    mission_statement = _("To provide customers of %(companyname)s in the %(companymarket)s market with the best possible value and customer experience, maintaining operational efficiency and providing a reasonable return for our shareholders and owners.") % {'companyname': company_name, 'companymarket': company_market}

    # Render.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        "OTHER_TEXT": OTHER_TEXT,
        'default_mission_statement': None
    }


@register.inclusion_tag('templatetags/question/template_013.html')
def render_question_type_014(workspace, module, node, question, answer):
    """
    DEPENDENCY:
    - template #001 | QTYPE_ID: 10 | geographic market
    - template #009 | QTYPE_ID: 11 | geographic market
    - template #011 | QTYPE_ID: 12 | naics
    """
    # Convert JSON string into python dictionary.
    picked = json.loads(answer.content)
    OTHER_TEXT = "Other (Please Specify)"

    # For this particular document and module, find the previous questions.
    q1_qid = int_or_none(question.dependency['q1_qid'])
    q2_qid = int_or_none(question.dependency['q2_qid'])
    q3_qid = int_or_none(question.dependency['q3_qid'])
    a1_raw = get_object_or_404(QuestionAnswer, question_id=q1_qid)
    a1 = json.loads(a1_raw.content)
    a2_raw = get_object_or_404(QuestionAnswer, question_id=q2_qid)
    a2 = json.loads(a2_raw.content)
    a3_raw = get_object_or_404(QuestionAnswer, question_id=q3_qid)
    a3 = json.loads(a3_raw.content)

    # 2. Generate geographic info.
    company_market = a2['var_1']

    # 3. Generate industry.
    naics_id = int(a3['var_5'])
    naic_option = NAICSOption.objects.get(id=naics_id)
    companyindustry = naic_option.name

    # 3. Generate text.
    mission_statement = _("To become the company of choice in %(companyindustry)s in the %(companymarket)s market.") % {'companyindustry': companyindustry, 'companymarket': company_market}

    # Render.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        "OTHER_TEXT": OTHER_TEXT,
        'default_mission_statement': mission_statement
    }


@register.inclusion_tag('templatetags/question/template_014.html')
def render_question_type_015(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': json.loads(answer.content),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_015.html')
def render_question_type_016(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_016.html')
def render_question_type_017(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_017.html')
def render_question_type_018(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked),
        'OTHER_TEXT': "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_018.html')
def render_question_type_019(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked),
        'OTHER_TEXT': "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_019.html')
def render_question_type_020(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_020.html')
def render_question_type_021(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_022.html')
def render_question_type_022(workspace, module, node, question, answer):
    """
    - Updates workspace as well.
    """
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_023.html')
def render_question_type_023(workspace, module, node, question, answer):
    """
    - uploads an image.
    """
    picked = json.loads(answer.content)

    # Fetch the image that is associated with this question's answer.
    imageupload = None
    if bool(picked):
        upload_id = int_or_none(picked['var_2'])
        if upload_id:
            imageupload = TenantImageUpload.objects.get(id=upload_id)

    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked),
        'imageupload': imageupload
    }


@register.inclusion_tag('templatetags/question/template_024.html')
def render_question_type_024(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_025.html')
def render_question_type_025(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_026.html')
def render_question_type_026(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_027.html')
def render_question_type_027(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_028.html')
def render_question_type_028(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_029.html')
def render_question_type_029(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_030.html')
def render_question_type_030(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_031.html')
def render_question_type_031(workspace, module, node, question, answer):
    x_pk = question.dependency['x_pk'] # Given
    y_pk = question.dependency['y_pk'] # Actual
    compare = question.dependency['compare']

    x_question = Question.objects.get(pk=x_pk)
    y_question = Question.objects.get(pk=y_pk)

    # Fetch the answer.
    x_answer = QuestionAnswer.objects.get(
        workspace=workspace,
        question_id=x_pk
    )
    y_answer = QuestionAnswer.objects.get(
        workspace=workspace,
        question_id=y_pk
    )

    # Extract the previously selected answer values.
    x_picked = json.loads(x_answer.content)
    y_picked = json.loads(y_answer.content)

    # Get the values
    x = 0
    if x_picked['var_1_other']:
        x = int(x_picked['var_1_other'])
    else:
        x = int(x_picked['var_1'])

    y = 0
    if y_picked['var_1_other']:
        y = int(y_picked['var_1_other'])
    else:
        y = int(y_picked['var_1'])

    # Perform our comparison.
    x_compare_y_result = False
    if compare == "<=":
        if x <= y:
            x_compare_y_result = True

    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked),
        'x_compare_y_result': x_compare_y_result,
    }


@register.inclusion_tag('templatetags/question/template_032.html')
def render_question_type_032(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_033.html')
def render_question_type_033(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }



@register.inclusion_tag('templatetags/question/template_034.html')
def render_question_type_034(workspace, module, node, question, answer):
    """
    DEPENDENCY:
    - QTYPE_ID: 31 | Will you offer mainly products, services, or both
    - QTYPE_ID: 32 | lease list at least 1, but up to 3 product or service categories that you will offer.
    """
    # Convert JSON string into python dictionary.
    picked = json.loads(answer.content)
    OTHER_TEXT = "Other (Please Specify)"

    # For this particular document and module, find the previous questions.
    q1_qid = int_or_none(question.dependency['q1_qid'])
    q2_qid = int_or_none(question.dependency['q2_qid'])
    a1_raw = get_object_or_404(QuestionAnswer, question_id=q1_qid)
    a1 = json.loads(a1_raw.content)
    a2_raw = get_object_or_404(QuestionAnswer, question_id=q2_qid)
    a2 = json.loads(a2_raw.content)

    # 2. Generate info.
    offer_category = a1['var_1']
    offer_1 = a2['var_1']
    offer_2 = a2['var_2']
    offer_3 = a2['var_3']

    # Render.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        "OTHER_TEXT": OTHER_TEXT,
        'offer_category': offer_category,
        'offer_1': offer_1,
        'offer_2': offer_2,
        'offer_3': offer_3
    }


@register.inclusion_tag('templatetags/question/template_035.html')
def render_question_type_035(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_036.html')
def render_question_type_036(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_037.html')
def render_question_type_037(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_038.html')
def render_question_type_038(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_039.html')
def render_question_type_039(workspace, module, node, question, answer):
    """
    DEPENDENCY:
    - QID: 32 | product categories
    """
    # Fetch the dependency answer.
    q1_qid = int_or_none(question.dependency['q1_qid'])
    dependent_answer = get_object_or_404(QuestionAnswer, question_id=q1_qid)

    # JSONIFY our previous answer.
    picked = json.loads(answer.content)
    dependent_answer = json.loads(dependent_answer.content)

    # Render our template.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked),
        'dependent_answer': dependent_answer
    }


@register.inclusion_tag('templatetags/question/template_040.html')
def render_question_type_040(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_041.html')
def render_question_type_041(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_042.html')
def render_question_type_042(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_043.html')
def render_question_type_043(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_044.html')
def render_question_type_044(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_045.html')
def render_question_type_045(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }


@register.inclusion_tag('templatetags/question/template_046.html')
def render_question_type_046(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked)
    }
