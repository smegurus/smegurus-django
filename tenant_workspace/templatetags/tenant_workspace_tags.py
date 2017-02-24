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


@register.simple_tag
def get_percent_by_module_and_node(module, node):
    rate = node['order_num'] / len(module.nodes)
    percent = int(rate * 100)
    return percent


@register.simple_tag
def reverse_previous_node(workspace, module, node):
    if node['previous_position'] == -1:
        return reverse('tenant_workspace_module_start_master', args=[workspace.id, module.id,])
    else:
        return reverse('tenant_workspace_module_detail', args=[workspace.id, module.id, node['previous_position'],])


@register.simple_tag
def reverse_next_node(workspace, module, node):
    if node['next_position'] == -1:
        return reverse('tenant_workspace_module_submit_master', args=[workspace.id, module.id, 0])
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
        'picked': answer.content
    }


@register.inclusion_tag('templatetags/question/template_002.html')
def render_question_type_002(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_003.html')
def render_question_type_003(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_004.html')
def render_question_type_004(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content),
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
        'picked': answer.content,
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_006.html')
def render_question_type_006(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content),
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
        'picked': answer.content,
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_008.html')
def render_question_type_008(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content),
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
    previous_question_answer = QuestionAnswer.objects.get(
        question_id=previous_question_id,
        workspace=workspace
    )

    # Input the variables into the template and render the view.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'previous_picked': previous_question_answer.content,
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_010.html')
def render_question_type_010(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_011.html')
def render_question_type_011(workspace, module, node, question, answer):
    # Fetch the image that is associated with this question's answer.
    imageupload = None
    upload_id = answer.content.get('var_2', None)
    if upload_id:
        upload_id = int_or_none(upload_id)
        imageupload = ImageUpload.objects.get(id=upload_id)

    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'imageupload': imageupload,
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_012.html')
def render_question_type_012(workspace, module, node, question, answer):
    """
    DEPENDENCY:
    - NAICSOption
    """
    picked = answer.content

    # If the answer was not created then we will pre-create the format.
    if not bool(picked): # We might need to change this
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
        'picked': answer.content,
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
    - QID: 61 | company name
    - QID: 10 | geographic market
    - QID: 11 | geographic market
    - NAICSOption
    """
    picked = answer.content

    # For this particular document and module, find the previous questions.
    q1_qid = int_or_none(question.dependency['q1_qid'])
    q2_qid = int_or_none(question.dependency['q2_qid'])
    q3_qid = int_or_none(question.dependency['q3_qid'])

    # --- Q1 ---
    a1_raw = QuestionAnswer.objects.get(
        question_id=q1_qid,
        workspace=workspace
    )
    a1 = a1_raw.content

    # --- Q2 ---
    a2_raw = QuestionAnswer.objects.get(
        question_id=q2_qid,
        workspace=workspace
    )
    a2 = None
    if a2_raw.content:
        a2 = a2_raw.content

    # --- Q3 ---
    a3_raw = QuestionAnswer.objects.get(
        question_id=q3_qid,
        workspace=workspace
    )
    geographic_market_details = None
    if a3_raw.content:
        geographic_market_details = a3_raw.content

    print(geographic_market_details)

    # Generate custom text from previous questions.
    # 1. Generate company name.
    company_name = a1['var_1']
    has_short_name = bool(a1['var_2'])
    if has_short_name:
        company_name = a1['var_3']

    # 2. Generate geographic info.
    company_market = None # Note: Handle "Online" and "Worldwide".
    if geographic_market_details['var_1_other']:
        company_market = geographic_market_details['var_1_other']
    else:
        if geographic_market_details['var_1']:
            company_market = geographic_market_details['var_1']
        else:
            company_market = geographic_market_details['var_0']

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
        'default_mission_statement': mission_statement
    }


@register.inclusion_tag('templatetags/question/template_013.html')
def render_question_type_014(workspace, module, node, question, answer):
    """
    DEPENDENCY:
    - template #001 | QTYPE_ID: 10 | geographic market
    - template #009 | QTYPE_ID: 11 | geographic market
    - template #011 | QTYPE_ID: 12 | naics
    """
    picked = answer.content

    # For this particular document and module, find the previous questions.
    q1_qid = int_or_none(question.dependency['q1_qid'])
    q2_qid = int_or_none(question.dependency['q2_qid'])
    q3_qid = int_or_none(question.dependency['q3_qid'])
    a1_raw = QuestionAnswer.objects.get(
        question_id=q1_qid,
        workspace=workspace
    )
    a1 = a1_raw.content
    a2_raw = QuestionAnswer.objects.get(
        question_id=q2_qid,
        workspace=workspace
    )
    a2 = a2_raw.content
    a3_raw = QuestionAnswer.objects.get(
        question_id=q3_qid,
        workspace=workspace
    )
    a3 = a3_raw.content

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
        'picked': answer.content,
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_015.html')
def render_question_type_016(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_016.html')
def render_question_type_017(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_017.html')
def render_question_type_018(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content),
        'OTHER_TEXT': "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_018.html')
def render_question_type_019(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content),
        'OTHER_TEXT': "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/template_019.html')
def render_question_type_020(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_020.html')
def render_question_type_021(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_022.html')
def render_question_type_022(workspace, module, node, question, answer):
    """
    - Updates workspace as well.
    """
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_023.html')
def render_question_type_023(workspace, module, node, question, answer):
    """
    - uploads an image.
    """
    # Fetch the image that is associated with this question's answer.
    imageupload = None
    upload_id = answer.content.get('var_2', None)
    if upload_id:
        imageupload = ImageUpload.objects.get(id=upload_id)

    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content),
        'imageupload': imageupload
    }


@register.inclusion_tag('templatetags/question/template_024.html')
def render_question_type_024(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_025.html')
def render_question_type_025(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_026.html')
def render_question_type_026(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_027.html')
def render_question_type_027(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_028.html')
def render_question_type_028(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_029.html')
def render_question_type_029(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_030.html')
def render_question_type_030(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
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
    x_picked = x_answer.content
    y_picked = y_answer.content

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

    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content),
        'x_compare_y_result': x_compare_y_result,
    }


@register.inclusion_tag('templatetags/question/template_032.html')
def render_question_type_032(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_033.html')
def render_question_type_033(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }



@register.inclusion_tag('templatetags/question/template_034.html')
def render_question_type_034(workspace, module, node, question, answer):
    """
    DEPENDENCY:
    - QTYPE_ID: 31 | Will you offer mainly products, services, or both
    - QTYPE_ID: 32 | lease list at least 1, but up to 3 product or service categories that you will offer.
    """
    picked = answer.content
    OTHER_TEXT = "Other (Please Specify)"

    # For this particular document and module, find the previous questions.
    q1_qid = int_or_none(question.dependency['q1_qid'])
    q2_qid = int_or_none(question.dependency['q2_qid'])
    a1_raw = QuestionAnswer.objects.get(
        question_id=q1_qid,
        workspace=workspace
    )
    a1 = a1_raw.content
    a2_raw = QuestionAnswer.objects.get(
        question_id=q2_qid,
        workspace=workspace
    )
    a2 = a2_raw.content

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
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_036.html')
def render_question_type_036(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_037.html')
def render_question_type_037(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_038.html')
def render_question_type_038(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_039.html')
def render_question_type_039(workspace, module, node, question, answer):
    """
    DEPENDENCY:
    - QID: 32 | product categories
    """
    # Fetch the dependency answer.
    q1_qid = int_or_none(question.dependency['q1_qid'])
    dependent_answer = QuestionAnswer.objects.get(
        question_id=q1_qid,
        workspace=workspace
    )

    dependent_answer = dependent_answer.content

    # Render our template.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content),
        'dependent_answer': dependent_answer
    }


@register.inclusion_tag('templatetags/question/template_040.html')
def render_question_type_040(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_041.html')
def render_question_type_041(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_042.html')
def render_question_type_042(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_043.html')
def render_question_type_043(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_044.html')
def render_question_type_044(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_045.html')
def render_question_type_045(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_047.html')
def render_question_type_047(workspace, module, node, question, answer):
    """
    DEPENDENCY:
    - QID: 32 | Product Categories
    - QID: 99 | Total Sales Volume
    """
    # Fetch the dependency answer.
    q1_qid = int_or_none(question.dependency['q1_qid'])
    q1_answer = QuestionAnswer.objects.get(
        question_id=q1_qid,
        workspace=workspace
    )
    q2_qid = int_or_none(question.dependency['q2_qid'])
    q2_answer = QuestionAnswer.objects.get(
        question_id=q2_qid,
        workspace=workspace
    )

    # Render our template.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'q1_answer': q1_answer.content,
        'q2_answer': q2_answer.content
    }


@register.inclusion_tag('templatetags/question/template_048.html')
def render_question_type_048(workspace, module, node, question, answer):
    """
    DEPENDENCY:
    - QID: 49 | My target market is based on...
    - QID: 99 | Total Sales Volume
    """
    # Fetch the dependency answer.
    q1_qid = int_or_none(question.dependency['q1_qid'])
    q1_answer = QuestionAnswer.objects.get(
        question_id=q1_qid,
        workspace=workspace
    )
    q2_qid = int_or_none(question.dependency['q2_qid'])
    q2_answer = QuestionAnswer.objects.get(
        question_id=q2_qid,
        workspace=workspace
    )

    # Render our template.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_len': len(answer.content),
        'q1_answer': q1_answer.content,
        'q1_answer_len': len(q1_answer.content),
        'q2_answer': q2_answer.content,
    }


@register.inclusion_tag('templatetags/question/template_050.html')
def render_question_type_050(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_049.html')
def render_question_type_051(workspace, module, node, question, answer):
    """
    DEPENDENCY:
    - QID: 105 | Please list salary expenses for all positions, including owners, broken down from years 1-3, with details on each position.
    OR
    - QID: 85 | Will you have any legal or professional fees to set up your business? If so, please detail them below.
    OR
    - QID: 108 | Please list your transportation costs and details from years 1-3.
    OR
    - QID: 86 | Will you have any ongoing location specific costs?
    OR
    - QID: 90 | Please list up to 5 licenses, registrations, or permits that you need to operate your business
    OR
    - QID: 114 | Please list all types of insurance, broken down from years 1-3, with details and costs for each.
    OR
    - QID: 116 | Please list your banking costs from years 1-3, with details and cost on each.
    OR
    - QID: 118 | Please list your general supplies costs from years 1-3, with details and cost on each.
    OR
    - QID: 120 | Please list your communications costs from years 1-3, with details and cost on each.
    OR
    - QID: 122 | Most businesses have tools, equipment and software subscriptions they pay for monthly or annually that they need to run their business ...
    OR
    - QID: 124 | Some businesses may have expenses associated with getting a customer to buy a product ...
    """
    # For this particular document and module, find the previous questions.
    q1_qid = int_or_none(question.dependency['q1_qid'])

    # Fetch Q1
    q1 = QuestionAnswer.objects.get(
        question_id=q1_qid,
        workspace=workspace
    )
    q1_picked = q1.content

    # Calculate annual totals.
    total_yr1 = 0.0
    total_yr2 = 0.0
    total_yr3 = 0.0
    for item in q1_picked:
        total_yr1 += float(item['var_5'])
        total_yr2 += float(item['var_6'])
        total_yr3 += float(item['var_7'])

    autogen = {
        # --- YEAR 1 ---
        'yr_1': total_yr1,
        'm_01': total_yr1 / 12.00,
        'm_02': total_yr1 / 12.00,
        'm_03': total_yr1 / 12.00,
        'm_04': total_yr1 / 12.00,
        'm_05': total_yr1 / 12.00,
        'm_06': total_yr1 / 12.00,
        'm_07': total_yr1 / 12.00,
        'm_08': total_yr1 / 12.00,
        'm_09': total_yr1 / 12.00,
        'm_10': total_yr1 / 12.00,
        'm_11': total_yr1 / 12.00,
        'm_12': total_yr1 / 12.00,

        # --- YEAR 2 ---
        'yr_2': total_yr2,
        'm_13': total_yr2 / 12.00,
        'm_14': total_yr2 / 12.00,
        'm_15': total_yr2 / 12.00,
        'm_16': total_yr2 / 12.00,
        'm_17': total_yr2 / 12.00,
        'm_18': total_yr2 / 12.00,
        'm_19': total_yr2 / 12.00,
        'm_20': total_yr2 / 12.00,
        'm_21': total_yr2 / 12.00,
        'm_22': total_yr2 / 12.00,
        'm_23': total_yr2 / 12.00,
        'm_24': total_yr2 / 12.00,

        # --- YEAR 3 ---
        'yr_3': total_yr3,
        'm_25': total_yr3 / 12.00,
        'm_26': total_yr3 / 12.00,
        'm_27': total_yr3 / 12.00,
        'm_28': total_yr3 / 12.00,
        'm_29': total_yr3 / 12.00,
        'm_30': total_yr3 / 12.00,
        'm_31': total_yr3 / 12.00,
        'm_32': total_yr3 / 12.00,
        'm_33': total_yr3 / 12.00,
        'm_34': total_yr3 / 12.00,
        'm_35': total_yr3 / 12.00,
        'm_36': total_yr3 / 12.00
    }

    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'answer_picked': answer.content,
        'autogen': autogen
    }


@register.inclusion_tag('templatetags/question/template_052.html')
def render_question_type_052(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_053.html')
def render_question_type_053(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_054.html')
def render_question_type_054(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_055.html')
def render_question_type_055(workspace, module, node, question, answer):
    """
    DEPENDENCY:
    - QID: 101 | We have taken your material, labour and overhead costs and spread them out based on the volume of product you told us for months 1-36.
    """
    # For this particular document and module, find the previous questions.
    q1_qid = int_or_none(question.dependency['q1_qid'])

    # Fetch Q1
    q1 = QuestionAnswer.objects.get(
        question_id=q1_qid,
        workspace=workspace
    )
    dependent_picked = q1.content

    # View template.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content),
        'dependent_picked': dependent_picked
    }


@register.inclusion_tag('templatetags/question/template_056.html')
def render_question_type_056(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_059.html')
def render_question_type_059(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_060.html')
def render_question_type_060(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content)
    }


@register.inclusion_tag('templatetags/question/template_061.html')
def render_question_type_061(workspace, module, node, question, answer):
    """
    - uploads an image.
    """
    # Fetch the image that is associated with this question's answer.
    imageupload = None
    upload_id = answer.content.get('var_2', None)
    if upload_id:
        imageupload = ImageUpload.objects.get(id=upload_id)

    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
        'picked_count': len(answer.content),
        'imageupload': imageupload
    }
