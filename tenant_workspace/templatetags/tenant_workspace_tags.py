# -*- coding: utf-8 -*-
import json
from django import template
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from foundation_tenant.utils import int_or_none
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


@register.inclusion_tag('templatetags/question/render_question_001.html')
def render_question_001(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': json.loads(answer.content),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/render_question_002.html')
def render_question_002(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': json.loads(answer.content),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/render_question_003.html')
def render_question_003(workspace, module, node, question, answer):
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


@register.inclusion_tag('templatetags/question/render_question_004.html')
def render_question_004(workspace, module, node, question, answer):
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


@register.inclusion_tag('templatetags/question/render_question_005.html')
def render_question_005(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': json.loads(answer.content),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/render_question_006.html')
def render_question_006(workspace, module, node, question, answer):
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


@register.inclusion_tag('templatetags/question/render_question_007.html')
def render_question_007(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': json.loads(answer.content),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/render_question_008.html')
def render_question_008(workspace, module, node, question, answer):
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


@register.inclusion_tag('templatetags/question/render_question_009.html')
def render_question_009(workspace, module, node, question, answer):
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


@register.inclusion_tag('templatetags/question/render_question_010.html')
def render_question_010(workspace, module, node, question, answer):
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


@register.inclusion_tag('templatetags/question/render_question_011.html')
def render_question_011(workspace, module, node, question, answer):
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


@register.inclusion_tag('templatetags/question/render_question_012.html')
def render_question_012(workspace, module, node, question, answer):
    """
    DEPENDENCY:
    - template #002 | QID: 02 | company name
    - template #001 | QID: 10 | geographic market
    - template #009 | QID: 11 | geographic market
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
    company_market = a3['var_1']

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
        'default_mission_statement': mission_statement
    }


    @register.inclusion_tag('templatetags/question/render_question_012.html')
    def render_question_013(workspace, module, node, question, answer):
        """
        DEPENDENCY:
        - template #002 | QID: 02 | company name
        - template #001 | QID: 10 | geographic market
        - template #009 | QID: 11 | geographic market
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
        company_market = a3['var_1']

        #TODO: GET THE "COMPANY INDUSTRY" FROM NIACS question.

        # 3. Generate text.
        mission_statement = _("To become the company of choice in the %(comapnyindustry)s in the %(companymarket)s market.") % {'comapnyindustry': company_name, 'companymarket': company_market}

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
