from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.translation import get_language
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from foundation_tenant.utils import int_or_none
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.models.bizmula.workspace import Workspace
from foundation_tenant.models.bizmula.document import Document
from foundation_tenant.models.bizmula.module import Module
from foundation_tenant.models.bizmula.slide import Slide
from foundation_tenant.models.bizmula.exercise import Exercise
from foundation_tenant.models.bizmula.question import Question


@login_required(login_url='/en/login')
@tenant_configuration_required
def master_page_redirect(request, workspace_id, exercise_id):
    # Find the start question to begin our exercise on.
    exercise = get_object_or_404(Exercise, pk=int_or_none(exercise_id))
    start_question_id = exercise.next_question_id(0)

    # Redirect to the start question.
    url = reverse('tenant_workspace_exercise_detail', args=[workspace_id, exercise_id, start_question_id])
    return redirect(url)


@login_required(login_url='/en/login')
@tenant_configuration_required
def detail_page(request, workspace_id, exercise_id, question_id):
    # Find our objects.
    workspace = get_object_or_404(Workspace, pk=int_or_none(workspace_id))
    exercise = get_object_or_404(Exercise, pk=int_or_none(exercise_id))
    question_id = int_or_none(question_id)
    question = get_object_or_404(Question, pk=question_id)

    # Find the next question to load up.
    next_question_id = exercise.next_question_id(question_id)

    # Find the previous question
    previous_question_id = exercise.previous_question_id(question_id)

    # Render our question
    return render(request, 'tenant_workspace/exercise/detail/view.html',{
        'page': 'workspace',
        'workspace': workspace,
        'exercise': exercise,
        'question': question,
        'next_question_id': next_question_id,
        'previous_question_id': previous_question_id
    })



@login_required(login_url='/en/login')
@tenant_configuration_required
def last_detail_page_redirect(request, workspace_id, exercise_id):
    # Find the last question in our Exercise.
    exercise = get_object_or_404(Exercise, pk=int_or_none(exercise_id))
    question_id = exercise.last_question_id()

    # Get the last question.
    question = get_object_or_404(Question, pk=question_id)

    # Redirect to the last question.
    url = reverse('tenant_workspace_exercise_detail', args=[workspace_id, exercise_id, question_id])
    return redirect(url)
