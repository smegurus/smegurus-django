from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.views.decorators.http import condition
from rest_framework.authtoken.models import Token
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.models.base.faqitem import FAQItem
from foundation_tenant.models.base.faqgroup import FAQGroup


def generate_faqs():
    """Function will generate pre-determined FAQ questions"""
    # SECTION 1 of 2
    qa_a1 = FAQItem.objects.create(
        question_text='How can I change the color?',
        answer_text='<p>Donec congue sagittis mi sit amet tincidunt. Quisque sollicitudin massa vel erat tincidunt blandit. Curabitur quis leo nulla. Phasellus faucibus placerat luctus. Integer fermentum molestie massa at congue. Quisque quis quam dictum diam volutpat adipiscing.</p><p>Proin ut urna enim.</p>',
    )
    qa_a2 = FAQItem.objects.create(
        question_text='How can I change the color?',
        answer_text='<p>Donec congue sagittis mi sit amet tincidunt. Quisque sollicitudin massa vel erat tincidunt blandit. Curabitur quis leo nulla. Phasellus faucibus placerat luctus. Integer fermentum molestie massa at congue. Quisque quis quam dictum diam volutpat adipiscing.</p><p>Proin ut urna enim.</p>',
    )
    qa_a3 = FAQItem.objects.create(
        question_text='How can I change the color?',
        answer_text='<p>Donec congue sagittis mi sit amet tincidunt. Quisque sollicitudin massa vel erat tincidunt blandit. Curabitur quis leo nulla. Phasellus faucibus placerat luctus. Integer fermentum molestie massa at congue. Quisque quis quam dictum diam volutpat adipiscing.</p><p>Proin ut urna enim.</p>',
    )
    group1 = FAQGroup.objects.create(text="Some presale Questions",)
    group1.items.add(qa_a1)
    group1.items.add(qa_a2)
    group1.items.add(qa_a3)

    # SECTION 1 of 2
    qa_b1 = FAQItem.objects.create(
        question_text='How can I change the color?',
        answer_text='<p>Donec congue sagittis mi sit amet tincidunt. Quisque sollicitudin massa vel erat tincidunt blandit. Curabitur quis leo nulla. Phasellus faucibus placerat luctus. Integer fermentum molestie massa at congue. Quisque quis quam dictum diam volutpat adipiscing.</p><p>Proin ut urna enim.</p>',
    )
    qa_b2 = FAQItem.objects.create(
        question_text='How can I change the color?',
        answer_text='<p>Donec congue sagittis mi sit amet tincidunt. Quisque sollicitudin massa vel erat tincidunt blandit. Curabitur quis leo nulla. Phasellus faucibus placerat luctus. Integer fermentum molestie massa at congue. Quisque quis quam dictum diam volutpat adipiscing.</p><p>Proin ut urna enim.</p>',
    )
    qa_b3 = FAQItem.objects.create(
        question_text='How can I change the color?',
        answer_text='<p>Donec congue sagittis mi sit amet tincidunt. Quisque sollicitudin massa vel erat tincidunt blandit. Curabitur quis leo nulla. Phasellus faucibus placerat luctus. Integer fermentum molestie massa at congue. Quisque quis quam dictum diam volutpat adipiscing.</p><p>Proin ut urna enim.</p>',
    )
    group2 = FAQGroup.objects.create(text="Buyer Questions",)
    group2.items.add(qa_b1)
    group2.items.add(qa_b2)
    group2.items.add(qa_b3)


# def latest_faq_master(request):
#     try:
#         return FAQGroup.objects.latest("last_modified").last_modified
#     except FAQGroup.DoesNotExist:
#         return datetime.now()


@login_required(login_url='/en/login')
@tenant_profile_required
# @condition(last_modified_func=latest_faq_master)
def faq_page(request):
    # FAQItem.objects.delete_all()
    # FAQGroup.objects.delete_all() # For debugging purposes only!

    faq_groups = FAQGroup.objects.all()
    if faq_groups.count() == 0:
        generate_faqs()
        faq_groups = FAQGroup.objects.all()

    return render(request, 'tenant_faq/view.html',{
        'faq_groups': faq_groups,
        'page': 'faq',
    })
