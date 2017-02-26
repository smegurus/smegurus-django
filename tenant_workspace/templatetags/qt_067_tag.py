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


register = template.Library()  # Register our custom template tag.


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


def get_processed_row(data, key):
    """
    Utility function will pick either the custom overriden value or the default
    value for the row.
    """
    if data[key+'_r']:
        return data[key+'_r']
    else:
        return data[key]


def get_processed_table(data):
    """
    Utility function for taking a table and picking the custom overriden values
    or the default values for the entire table.
    """
    # Take the row and see if we are to use a custom value or the default value.
    arr = {
        # Year 1
        'm_01':  get_processed_row(data, 'm_01'),
        'm_02':  get_processed_row(data, 'm_02'),
        'm_03':  get_processed_row(data, 'm_03'),
        'm_04':  get_processed_row(data, 'm_04'),
        'm_05':  get_processed_row(data, 'm_05'),
        'm_06':  get_processed_row(data, 'm_06'),
        'm_07':  get_processed_row(data, 'm_07'),
        'm_08':  get_processed_row(data, 'm_08'),
        'm_09':  get_processed_row(data, 'm_09'),
        'm_10':  get_processed_row(data, 'm_10'),
        'm_11':  get_processed_row(data, 'm_11'),
        'm_12':  get_processed_row(data, 'm_12'),
        'yr_1':  get_processed_row(data, 'yr_1'),

        # Year 2
        'm_13':  get_processed_row(data, 'm_13'),
        'm_14':  get_processed_row(data, 'm_14'),
        'm_15':  get_processed_row(data, 'm_15'),
        'm_16':  get_processed_row(data, 'm_16'),
        'm_17':  get_processed_row(data, 'm_17'),
        'm_18':  get_processed_row(data, 'm_18'),
        'm_19':  get_processed_row(data, 'm_19'),
        'm_20':  get_processed_row(data, 'm_20'),
        'm_21':  get_processed_row(data, 'm_21'),
        'm_22':  get_processed_row(data, 'm_22'),
        'm_23':  get_processed_row(data, 'm_23'),
        'm_24':  get_processed_row(data, 'm_24'),
        'yr_2':  get_processed_row(data, 'yr_2'),

        # Year 3
        'm_25':  get_processed_row(data, 'm_25'),
        'm_26':  get_processed_row(data, 'm_26'),
        'm_27':  get_processed_row(data, 'm_27'),
        'm_28':  get_processed_row(data, 'm_28'),
        'm_29':  get_processed_row(data, 'm_29'),
        'm_30':  get_processed_row(data, 'm_30'),
        'm_31':  get_processed_row(data, 'm_31'),
        'm_32':  get_processed_row(data, 'm_32'),
        'm_33':  get_processed_row(data, 'm_33'),
        'm_34':  get_processed_row(data, 'm_34'),
        'm_35':  get_processed_row(data, 'm_35'),
        'm_36':  get_processed_row(data, 'm_36'),
        'yr_3':  get_processed_row(data, 'yr_3')
    }
    # Find any 'None' values and replace them with zeros.
    return {
        # Year 1
        'm_01':  0 if arr['m_01'] == None else arr['m_01'],
        'm_02':  0 if arr['m_02'] == None else arr['m_02'],
        'm_03':  0 if arr['m_03'] == None else arr['m_03'],
        'm_04':  0 if arr['m_04'] == None else arr['m_04'],
        'm_05':  0 if arr['m_05'] == None else arr['m_05'],
        'm_06':  0 if arr['m_06'] == None else arr['m_06'],
        'm_07':  0 if arr['m_07'] == None else arr['m_07'],
        'm_08':  0 if arr['m_08'] == None else arr['m_08'],
        'm_09':  0 if arr['m_09'] == None else arr['m_09'],
        'm_10':  0 if arr['m_10'] == None else arr['m_10'],
        'm_11':  0 if arr['m_11'] == None else arr['m_11'],
        'm_12':  0 if arr['m_12'] == None else arr['m_12'],
        'yr_1':  0 if arr['yr_1'] == None else arr['yr_1'],

        # Year 2
        'm_13':  0 if arr['m_13'] == None else arr['m_13'],
        'm_14':  0 if arr['m_14'] == None else arr['m_14'],
        'm_15':  0 if arr['m_15'] == None else arr['m_15'],
        'm_16':  0 if arr['m_16'] == None else arr['m_16'],
        'm_17':  0 if arr['m_17'] == None else arr['m_17'],
        'm_18':  0 if arr['m_18'] == None else arr['m_18'],
        'm_19':  0 if arr['m_19'] == None else arr['m_19'],
        'm_20':  0 if arr['m_20'] == None else arr['m_20'],
        'm_21':  0 if arr['m_21'] == None else arr['m_21'],
        'm_22':  0 if arr['m_22'] == None else arr['m_22'],
        'm_23':  0 if arr['m_23'] == None else arr['m_23'],
        'm_24':  0 if arr['m_24'] == None else arr['m_24'],
        'yr_2':  0 if arr['yr_2'] == None else arr['yr_2'],

        # Year 3
        'm_25':  0 if arr['m_25'] == None else arr['m_25'],
        'm_26':  0 if arr['m_26'] == None else arr['m_26'],
        'm_27':  0 if arr['m_27'] == None else arr['m_27'],
        'm_28':  0 if arr['m_28'] == None else arr['m_28'],
        'm_29':  0 if arr['m_29'] == None else arr['m_29'],
        'm_30':  0 if arr['m_30'] == None else arr['m_30'],
        'm_31':  0 if arr['m_31'] == None else arr['m_31'],
        'm_32':  0 if arr['m_32'] == None else arr['m_32'],
        'm_33':  0 if arr['m_33'] == None else arr['m_33'],
        'm_34':  0 if arr['m_34'] == None else arr['m_34'],
        'm_35':  0 if arr['m_35'] == None else arr['m_35'],
        'm_36':  0 if arr['m_36'] == None else arr['m_36'],
        'yr_3':  0 if arr['yr_3'] == None else arr['yr_3']
    }


def get_table_for_qid(workspace, qid):
    """
    Utility function will get the (processed) table data for the yr1, yr2, yr3
    table answer.
    """
    answer = QuestionAnswer.objects.get(
        question_id=qid,
        workspace=workspace
    )
    return get_processed_table(answer.content)


def get_table_for_qid_163(workspace, q19_qid):
    q19 = QuestionAnswer.objects.get(
        question_id=q19_qid,
        workspace=workspace
    )
    q19 = q19.content
    return {
        # - - - - - - - - - - - - - - # YEAR 1 # - - - - - - - - - - - - - - #
        'total_sales_m1': q19['m1'], 'total_sales_m2': q19['m2'], 'total_sales_m3': q19['m3'],
        'total_sales_m4': q19['m4'], 'total_sales_m5': q19['m5'], 'total_sales_m6': q19['m6'],
        'total_sales_m7': q19['m7'], 'total_sales_m8': q19['m8'], 'total_sales_m9': q19['m9'],
        'total_sales_m10': q19['m10'], 'total_sales_m11': q19['m11'], 'total_sales_m12': q19['m12'],
        'total_sales_y1': q19['yr1_total'],

        # - - - - - - - - - - - - - - # YEAR 2 # - - - - - - - - - - - - - - #
        'total_sales_m13': q19['m13'], 'total_sales_m14': q19['m14'], 'total_sales_m15': q19['m15'],
        'total_sales_m16': q19['m16'], 'total_sales_m17': q19['m17'], 'total_sales_m18': q19['m18'],
        'total_sales_m19': q19['m19'], 'total_sales_m20': q19['m20'], 'total_sales_m21': q19['m21'],
        'total_sales_m22': q19['m22'], 'total_sales_m23': q19['m23'], 'total_sales_m24': q19['m24'],
        'total_sales_y2': q19['yr2_total'],

        # - - - - - - - - - - - - - - # YEAR 3 # - - - - - - - - - - - - - - #
        'total_sales_m25': q19['m25'], 'total_sales_m26': q19['m26'], 'total_sales_m27': q19['m27'],
        'total_sales_m28': q19['m28'], 'total_sales_m29': q19['m29'], 'total_sales_m30': q19['m30'],
        'total_sales_m31': q19['m31'], 'total_sales_m32': q19['m32'], 'total_sales_m33': q19['m33'],
        'total_sales_m34': q19['m34'], 'total_sales_m35': q19['m35'], 'total_sales_m36': q19['m36'],
        'total_sales_y3': q19['yr3_total'],
    }

def get_table_for_qid_101(workspace, qid):
    """
    Utility function will get the (processed) table data for the yr1, yr2, yr3
    table answer.
    """
    answer = QuestionAnswer.objects.get(
        question_id=qid,
        workspace=workspace
    )
    total_cogs = answer.content
    return {
        # - - - - - - - - - - - - - - # YEAR 1 # - - - - - - - - - - - - - - #
        'total_cogs_m1': total_cogs['total_month_1_other'] if total_cogs['total_month_1_other'] else total_cogs['total_month_1'],
        'total_cogs_m2': total_cogs['total_month_2_other'] if total_cogs['total_month_2_other'] else total_cogs['total_month_2'],
        'total_cogs_m3': total_cogs['total_month_3_other'] if total_cogs['total_month_3_other'] else total_cogs['total_month_3'],
        'total_cogs_m4': total_cogs['total_month_4_other'] if total_cogs['total_month_4_other'] else total_cogs['total_month_4'],
        'total_cogs_m5': total_cogs['total_month_5_other'] if total_cogs['total_month_5_other'] else total_cogs['total_month_5'],
        'total_cogs_m6': total_cogs['total_month_6_other'] if total_cogs['total_month_6_other'] else total_cogs['total_month_6'],
        'total_cogs_m7': total_cogs['total_month_7_other'] if total_cogs['total_month_7_other'] else total_cogs['total_month_7'],
        'total_cogs_m8': total_cogs['total_month_8_other'] if total_cogs['total_month_8_other'] else total_cogs['total_month_8'],
        'total_cogs_m9': total_cogs['total_month_9_other'] if total_cogs['total_month_9_other'] else total_cogs['total_month_9'],
        'total_cogs_m10': total_cogs['total_month_10_other'] if total_cogs['total_month_10_other'] else total_cogs['total_month_10'],
        'total_cogs_m11': total_cogs['total_month_11_other'] if total_cogs['total_month_11_other'] else total_cogs['total_month_11'],
        'total_cogs_m12': total_cogs['total_month_12_other'] if total_cogs['total_month_12_other'] else total_cogs['total_month_12'],
        'total_cogs_y1': total_cogs['total_year_1'],

        # - - - - - - - - - - - - - - # YEAR 2 # - - - - - - - - - - - - - - #
        'total_cogs_m13': total_cogs['total_month_13_other'] if total_cogs['total_month_13_other'] else total_cogs['total_month_13'],
        'total_cogs_m14': total_cogs['total_month_14_other'] if total_cogs['total_month_14_other'] else total_cogs['total_month_14'],
        'total_cogs_m15': total_cogs['total_month_15_other'] if total_cogs['total_month_15_other'] else total_cogs['total_month_15'],
        'total_cogs_m16': total_cogs['total_month_16_other'] if total_cogs['total_month_16_other'] else total_cogs['total_month_16'],
        'total_cogs_m17': total_cogs['total_month_17_other'] if total_cogs['total_month_17_other'] else total_cogs['total_month_17'],
        'total_cogs_m18': total_cogs['total_month_18_other'] if total_cogs['total_month_18_other'] else total_cogs['total_month_18'],
        'total_cogs_m19': total_cogs['total_month_19_other'] if total_cogs['total_month_19_other'] else total_cogs['total_month_19'],
        'total_cogs_m20': total_cogs['total_month_20_other'] if total_cogs['total_month_20_other'] else total_cogs['total_month_20'],
        'total_cogs_m21': total_cogs['total_month_21_other'] if total_cogs['total_month_21_other'] else total_cogs['total_month_21'],
        'total_cogs_m22': total_cogs['total_month_22_other'] if total_cogs['total_month_22_other'] else total_cogs['total_month_22'],
        'total_cogs_m23': total_cogs['total_month_23_other'] if total_cogs['total_month_23_other'] else total_cogs['total_month_23'],
        'total_cogs_m24': total_cogs['total_month_24_other'] if total_cogs['total_month_24_other'] else total_cogs['total_month_24'],
        'total_cogs_y2': total_cogs['total_year_2'],

        # - - - - - - - - - - - - - - # YEAR 3 # - - - - - - - - - - - - - - #
        'total_cogs_m25': total_cogs['total_month_25_other'] if total_cogs['total_month_25_other'] else total_cogs['total_month_25'],
        'total_cogs_m26': total_cogs['total_month_26_other'] if total_cogs['total_month_26_other'] else total_cogs['total_month_26'],
        'total_cogs_m27': total_cogs['total_month_27_other'] if total_cogs['total_month_27_other'] else total_cogs['total_month_27'],
        'total_cogs_m28': total_cogs['total_month_28_other'] if total_cogs['total_month_28_other'] else total_cogs['total_month_28'],
        'total_cogs_m29': total_cogs['total_month_29_other'] if total_cogs['total_month_29_other'] else total_cogs['total_month_29'],
        'total_cogs_m30': total_cogs['total_month_30_other'] if total_cogs['total_month_30_other'] else total_cogs['total_month_30'],
        'total_cogs_m31': total_cogs['total_month_31_other'] if total_cogs['total_month_31_other'] else total_cogs['total_month_31'],
        'total_cogs_m32': total_cogs['total_month_32_other'] if total_cogs['total_month_32_other'] else total_cogs['total_month_32'],
        'total_cogs_m33': total_cogs['total_month_33_other'] if total_cogs['total_month_33_other'] else total_cogs['total_month_33'],
        'total_cogs_m34': total_cogs['total_month_34_other'] if total_cogs['total_month_34_other'] else total_cogs['total_month_34'],
        'total_cogs_m35': total_cogs['total_month_35_other'] if total_cogs['total_month_35_other'] else total_cogs['total_month_35'],
        'total_cogs_m36': total_cogs['total_month_36_other'] if total_cogs['total_month_36_other'] else total_cogs['total_month_36'],
        'total_cogs_y3': total_cogs['total_year_3']
    }


def get_profit_margine(total_sales, total_cogs):
    return {
        # - - - - - - - - - - - - - - # YEAR 1 # - - - - - - - - - - - - - - #
        'gross_profit_m1': total_sales['total_sales_m1'] - total_cogs['total_cogs_m1'],
        'gross_profit_m2': total_sales['total_sales_m2'] - total_cogs['total_cogs_m2'],
        'gross_profit_m3': total_sales['total_sales_m3'] - total_cogs['total_cogs_m3'],
        'gross_profit_m4': total_sales['total_sales_m4'] - total_cogs['total_cogs_m4'],
        'gross_profit_m5': total_sales['total_sales_m5'] - total_cogs['total_cogs_m5'],
        'gross_profit_m6': total_sales['total_sales_m6'] - total_cogs['total_cogs_m6'],
        'gross_profit_m7': total_sales['total_sales_m7'] - total_cogs['total_cogs_m7'],
        'gross_profit_m8': total_sales['total_sales_m8'] - total_cogs['total_cogs_m8'],
        'gross_profit_m9': total_sales['total_sales_m9'] - total_cogs['total_cogs_m9'],
        'gross_profit_m10': total_sales['total_sales_m10'] - total_cogs['total_cogs_m10'],
        'gross_profit_m11': total_sales['total_sales_m11'] - total_cogs['total_cogs_m11'],
        'gross_profit_m12': total_sales['total_sales_m12'] - total_cogs['total_cogs_m12'],
        'gross_profit_yr1': total_sales['total_sales_y1'] - total_cogs['total_cogs_y1'],

        # - - - - - - - - - - - - - - # YEAR 2 # - - - - - - - - - - - - - - #
        'gross_profit_m13': total_sales['total_sales_m13'] - total_cogs['total_cogs_m13'],
        'gross_profit_m14': total_sales['total_sales_m14'] - total_cogs['total_cogs_m14'],
        'gross_profit_m15': total_sales['total_sales_m15'] - total_cogs['total_cogs_m15'],
        'gross_profit_m16': total_sales['total_sales_m16'] - total_cogs['total_cogs_m16'],
        'gross_profit_m17': total_sales['total_sales_m17'] - total_cogs['total_cogs_m17'],
        'gross_profit_m18': total_sales['total_sales_m18'] - total_cogs['total_cogs_m18'],
        'gross_profit_m19': total_sales['total_sales_m19'] - total_cogs['total_cogs_m19'],
        'gross_profit_m20': total_sales['total_sales_m20'] - total_cogs['total_cogs_m20'],
        'gross_profit_m21': total_sales['total_sales_m21'] - total_cogs['total_cogs_m21'],
        'gross_profit_m22': total_sales['total_sales_m22'] - total_cogs['total_cogs_m22'],
        'gross_profit_m23': total_sales['total_sales_m23'] - total_cogs['total_cogs_m23'],
        'gross_profit_m24': total_sales['total_sales_m24'] - total_cogs['total_cogs_m24'],
        'gross_profit_yr2': total_sales['total_sales_y2'] - total_cogs['total_cogs_y2'],

        # - - - - - - - - - - - - - - # YEAR 3 # - - - - - - - - - - - - - - #
        'gross_profit_m25': total_sales['total_sales_m25'] - total_cogs['total_cogs_m25'],
        'gross_profit_m26': total_sales['total_sales_m26'] - total_cogs['total_cogs_m26'],
        'gross_profit_m27': total_sales['total_sales_m27'] - total_cogs['total_cogs_m27'],
        'gross_profit_m28': total_sales['total_sales_m28'] - total_cogs['total_cogs_m28'],
        'gross_profit_m29': total_sales['total_sales_m29'] - total_cogs['total_cogs_m29'],
        'gross_profit_m30': total_sales['total_sales_m30'] - total_cogs['total_cogs_m30'],
        'gross_profit_m31': total_sales['total_sales_m31'] - total_cogs['total_cogs_m31'],
        'gross_profit_m32': total_sales['total_sales_m32'] - total_cogs['total_cogs_m32'],
        'gross_profit_m33': total_sales['total_sales_m33'] - total_cogs['total_cogs_m33'],
        'gross_profit_m34': total_sales['total_sales_m34'] - total_cogs['total_cogs_m34'],
        'gross_profit_m35': total_sales['total_sales_m35'] - total_cogs['total_cogs_m35'],
        'gross_profit_m36': total_sales['total_sales_m36'] - total_cogs['total_cogs_m36'],
        'gross_profit_yr3': total_sales['total_sales_y3'] - total_cogs['total_cogs_y3']
    }

def attach_table(computation, key, data):
    return merge_two_dicts(computation, {
        # - - - - - - - - - - - - - - # YEAR 1 # - - - - - - - - - - - - - - #
        key+'_m1': data['m_01'], key+'_m2': data['m_02'], key+'_m3': data['m_03'],
        key+'_m4': data['m_04'], key+'_m5': data['m_05'], key+'_m6': data['m_06'],
        key+'_m7': data['m_07'], key+'_m8': data['m_08'], key+'_m9': data['m_09'],
        key+'_m10': data['m_10'], key+'_m11': data['m_11'], key+'_m12': data['m_12'],
        key+'_yr1': data['yr_1'],

        # - - - - - - - - - - - - - - # YEAR 2 # - - - - - - - - - - - - - - #
        key+'_m13': data['m_13'], key+'_m14': data['m_14'], key+'_m15': data['m_15'],
        key+'_m16': data['m_16'], key+'_m17': data['m_17'], key+'_m18': data['m_18'],
        key+'_m19': data['m_19'], key+'_m20': data['m_20'], key+'_m21': data['m_21'],
        key+'_m22': data['m_22'], key+'_m23': data['m_23'], key+'_m24': data['m_24'],
        key+'_yr2': data['yr_2'],

        # - - - - - - - - - - - - - - # YEAR 3 # - - - - - - - - - - - - - - #
        key+'_m25': data['m_25'], key+'_m26': data['m_26'], key+'_m27': data['m_27'],
        key+'_m28': data['m_28'], key+'_m29': data['m_29'], key+'_m30': data['m_30'],
        key+'_m31': data['m_31'], key+'_m32': data['m_32'], key+'_m33': data['m_33'],
        key+'_m34': data['m_33'], key+'_m34': data['m_34'], key+'_m35': data['m_35'],
        key+'_m36': data['m_36'],
        key+'_yr3': data['yr_3']
    })


def sum_tables(array_1, array_2):
    return {
        # yr1
        'm_01': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_02': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_03': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_04': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_05': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_06': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_07': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_08': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_09': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_10': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_11': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_12': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'yr_1': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],

        # yr2
        'm_13': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_14': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_15': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_16': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_17': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_18': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_19': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_20': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_21': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_22': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_23': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_24': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'yr_2': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],

        # yr3
        'm_25': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_26': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_27': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_28': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_29': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_30': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_31': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_32': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_33': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_34': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_35': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'm_36': 0 if array_1['m_01'] == None else array_1['m_01'] + 0 if array_2['m_01'] == None else array_2['m_01'],
        'yr_3': array_1['yr_3'] + array_2['yr_3']
    }

def get_net_profit(array_1, array_2):
    return {
        # yr1
        'm_01': array_1['gross_profit_m1'] - array_2['m_01'],
        'm_02': array_1['gross_profit_m2'] - array_2['m_02'],
        'm_03': array_1['gross_profit_m3'] - array_2['m_03'],
        'm_04': array_1['gross_profit_m4'] - array_2['m_04'],
        'm_05': array_1['gross_profit_m5'] - array_2['m_05'],
        'm_06': array_1['gross_profit_m6'] - array_2['m_06'],
        'm_07': array_1['gross_profit_m7'] - array_2['m_07'],
        'm_08': array_1['gross_profit_m8'] - array_2['m_08'],
        'm_09': array_1['gross_profit_m9'] - array_2['m_09'],
        'm_10': array_1['gross_profit_m10'] - array_2['m_10'],
        'm_11': array_1['gross_profit_m11'] - array_2['m_11'],
        'm_12': array_1['gross_profit_m12'] - array_2['m_12'],
        'yr_1': array_1['gross_profit_yr1'] - array_2['yr_1'],

        # yr2
        'm_13': array_1['gross_profit_m13'] - array_2['m_13'],
        'm_14': array_1['gross_profit_m14'] - array_2['m_14'],
        'm_15': array_1['gross_profit_m15'] - array_2['m_15'],
        'm_16': array_1['gross_profit_m16'] - array_2['m_16'],
        'm_17': array_1['gross_profit_m17'] - array_2['m_17'],
        'm_18': array_1['gross_profit_m18'] - array_2['m_18'],
        'm_19': array_1['gross_profit_m19'] - array_2['m_19'],
        'm_20': array_1['gross_profit_m20'] - array_2['m_20'],
        'm_21': array_1['gross_profit_m21'] - array_2['m_21'],
        'm_22': array_1['gross_profit_m22'] - array_2['m_22'],
        'm_23': array_1['gross_profit_m23'] - array_2['m_23'],
        'm_24': array_1['gross_profit_m24'] - array_2['m_24'],
        'yr_2': array_1['gross_profit_yr2'] - array_2['yr_2'],

        # yr3
        'm_25': array_1['gross_profit_m25'] - array_2['m_25'],
        'm_26': array_1['gross_profit_m26'] - array_2['m_26'],
        'm_27': array_1['gross_profit_m27'] - array_2['m_27'],
        'm_28': array_1['gross_profit_m28'] - array_2['m_28'],
        'm_29': array_1['gross_profit_m29'] - array_2['m_29'],
        'm_30': array_1['gross_profit_m30'] - array_2['m_30'],
        'm_31': array_1['gross_profit_m31'] - array_2['m_31'],
        'm_32': array_1['gross_profit_m32'] - array_2['m_32'],
        'm_33': array_1['gross_profit_m33'] - array_2['m_33'],
        'm_34': array_1['gross_profit_m34'] - array_2['m_34'],
        'm_35': array_1['gross_profit_m35'] - array_2['m_35'],
        'm_36': array_1['gross_profit_m36'] - array_2['m_36'],
        'yr_3': array_1['gross_profit_yr3'] - array_2['yr_3']
    }


@register.inclusion_tag('templatetags/question/template_067.html')
def render_question_type_067(workspace, module, node, question, answer):
    #================================#
    # Fetch & pre-process questions. #
    #================================#

    # PK 101 - total_cogs_m1
    q1_qid = int_or_none(question.dependency['q1_qid'])
    total_cogs = get_table_for_qid_101(workspace, q1_qid)

    # PK 104 - Stage 7, Marketing Costs
    q2_qid = int_or_none(question.dependency['q2_qid'])
    marketing_costs = get_table_for_qid(workspace, q2_qid)

    # PK 108 - Salaries
    q3_qid = int_or_none(question.dependency['q3_qid'])
    q3 = QuestionAnswer.objects.get(
        question_id=q3_qid,
        workspace=workspace
    )
    q3 = q3.content
    total_yr1 = 0.0
    total_yr2 = 0.0
    total_yr3 = 0.0
    for item in q3:
        total_yr1 += float(item['var_5'])
        total_yr2 += float(item['var_6'])
        total_yr3 += float(item['var_7'])
    salaries = {
        'yr1': total_yr1,
        'yr2': total_yr2,
        'yr3': total_yr3
    }

    # PK107 - Pro Fees
    q4_qid = int_or_none(question.dependency['q4_qid'])
    pro_fees = get_table_for_qid(workspace, q4_qid)

    # PK112 - Admin. costs
    q5_qid = int_or_none(question.dependency['q5_qid'])
    admin_costs = get_table_for_qid(workspace, q5_qid)

    # PK125 - Sales expenses
    q6_qid = int_or_none(question.dependency['q6_qid'])
    sales_expenses = get_table_for_qid(workspace, q6_qid)

    # PK110 - Location specific costs
    q7_qid = int_or_none(question.dependency['q7_qid'])
    loc_specific_costs = get_table_for_qid(workspace, q7_qid)

    # PK115 - Insurance costs
    q8_qid = int_or_none(question.dependency['q8_qid'])
    insurance_costs = get_table_for_qid(workspace, q8_qid)

    # PK113 - License/Registration costs
    q9_qid = int_or_none(question.dependency['q9_qid'])
    license_reg_costs = get_table_for_qid(workspace, q9_qid)

    # PK109 - Transportation costs
    q10_qid = int_or_none(question.dependency['q10_qid'])
    transportation_costs = get_table_for_qid(workspace, q10_qid)

    # PK117 - Banking costs
    q11_qid = int_or_none(question.dependency['q11_qid'])
    banking_costs = get_table_for_qid(workspace, q11_qid)

    # PK119 - Office supplies
    q12_qid = int_or_none(question.dependency['q12_qid'])
    office_supplies_cost = get_table_for_qid(workspace, q12_qid)

    # PK121 - Communication Costs
    q13_qid = int_or_none(question.dependency['q13_qid'])
    communication_costs = get_table_for_qid(workspace, q13_qid)

    # PK127 - Membership fees
    q14_qid = int_or_none(question.dependency['q14_qid'])
    membership_fees = get_table_for_qid(workspace, q14_qid)

    # PK129 - Equipment lease
    q15_qid = int_or_none(question.dependency['q15_qid'])
    equipment_lease = get_table_for_qid(workspace, q15_qid)

    # PK131 - Maintenance
    q16_qid = int_or_none(question.dependency['q16_qid'])
    maintain_costs = get_table_for_qid(workspace, q16_qid)

    # PK133 - Other
    q17_qid = int_or_none(question.dependency['q17_qid'])
    other_costs = get_table_for_qid(workspace, q17_qid)

    # PK135 - Misc
    q18_qid = int_or_none(question.dependency['q18_qid'])
    misc_costs = get_table_for_qid(workspace, q18_qid)

    # PK163 - total_sales_m1
    q19_qid = int_or_none(question.dependency['q19_qid'])
    total_sales = get_table_for_qid_163(workspace, q19_qid)

    # PK167 - net_startup_deficit_surplus
    q20_qid = int_or_none(question.dependency['q20_qid'])
    q20 = QuestionAnswer.objects.get(
        question_id=q20_qid,
        workspace=workspace
    )
    q20 = q20.content

    # PK106 - Salaries
    q21_qid = int_or_none(question.dependency['q21_qid'])
    salaries = get_table_for_qid(workspace, q21_qid)

    # PK123 - Subscription
    q22_qid = int_or_none(question.dependency['q22_qid'])
    subscriptions = get_table_for_qid(workspace, q22_qid)

    #====================================#
    # Pre-Process question computations. #
    #====================================#
    gross_profit = get_profit_margine(total_sales, total_cogs)

    #================================#
    # Process question computations. #
    #================================#
    computation = {} # Variable to store our table.

    # Start-up Costs
    #------------------------

    # Start-Up Surplus/Deficit
    computation = merge_two_dicts(computation, {
        'net_startup_deficit_surplus': q20['net_startup_deficit_surplus'],
    })

    # Revenue
    #------------------------
    computation = merge_two_dicts(computation, total_sales)
    computation = merge_two_dicts(computation, total_cogs)
    computation = merge_two_dicts(computation, gross_profit)

    # General & Admin Expenses
    #------------------------
    computation= attach_table(computation, 'location_costs', loc_specific_costs)
    computation= attach_table(computation, 'insurance_costs', insurance_costs)
    computation= attach_table(computation, 'admin_costs', admin_costs)
    computation= attach_table(computation, 'license_costs', license_reg_costs)
    computation= attach_table(computation, 'marketing_costs', marketing_costs)
    computation= attach_table(computation, 'sales_expenses', sales_expenses)
    computation= attach_table(computation, 'bank_fees', banking_costs)
    computation= attach_table(computation, 'salary_costs', salaries)
    computation= attach_table(computation, 'comm_costs', communication_costs)
    computation= attach_table(computation, 'transportation_costs', transportation_costs)
    computation= attach_table(computation, 'sub_costs', subscriptions)
    computation= attach_table(computation, 'lease_costs', equipment_lease)
    computation= attach_table(computation, 'maintain_costs', maintain_costs)
    computation= attach_table(computation, 'supplies_costs', office_supplies_cost)
    computation= attach_table(computation, 'pro_fee_costs', pro_fees)
    computation= attach_table(computation, 'mem_costs', membership_fees)
    computation= attach_table(computation, 'other_costs', other_costs)
    computation= attach_table(computation, 'misc_costs', misc_costs)

    # Total G & A Expenses
    #------------------------
    total_g_a = sum_tables(loc_specific_costs, insurance_costs)
    total_g_a = sum_tables(total_g_a, admin_costs)
    total_g_a = sum_tables(total_g_a, license_reg_costs)
    total_g_a = sum_tables(total_g_a, marketing_costs)
    total_g_a = sum_tables(total_g_a, sales_expenses)
    total_g_a = sum_tables(total_g_a, banking_costs)
    total_g_a = sum_tables(total_g_a, salaries)
    total_g_a = sum_tables(total_g_a, communication_costs)
    total_g_a = sum_tables(total_g_a, transportation_costs)
    total_g_a = sum_tables(total_g_a, subscriptions)
    total_g_a = sum_tables(total_g_a, equipment_lease)
    total_g_a = sum_tables(total_g_a, maintain_costs)
    total_g_a = sum_tables(total_g_a, office_supplies_cost)
    total_g_a = sum_tables(total_g_a, pro_fees)
    total_g_a = sum_tables(total_g_a, membership_fees)
    total_g_a = sum_tables(total_g_a, other_costs)
    total_g_a = sum_tables(total_g_a, misc_costs)
    computation= attach_table(computation, 'total_g_a', total_g_a)

    # Net Profit
    #------------
    net_profit = get_net_profit(gross_profit, total_g_a)
    computation = attach_table(computation, 'net_profit', net_profit)

    # Net Cash Position
    #------------
    start = q20['net_startup_deficit_surplus']
    net_cash_position = {
        "net_cash_m0": start
    }
    #Yr1
    net_cash_position['net_cash_m1'] = net_cash_position['net_cash_m0'] + net_profit['m_01']
    net_cash_position['net_cash_m2'] = net_cash_position['net_cash_m1'] + net_profit['m_02']
    net_cash_position['net_cash_m3'] = net_cash_position['net_cash_m2'] + net_profit['m_03']
    net_cash_position['net_cash_m4'] = net_cash_position['net_cash_m3'] + net_profit['m_04']
    net_cash_position['net_cash_m5'] = net_cash_position['net_cash_m4'] + net_profit['m_05']
    net_cash_position['net_cash_m6'] = net_cash_position['net_cash_m5'] + net_profit['m_06']
    net_cash_position['net_cash_m7'] = net_cash_position['net_cash_m6'] + net_profit['m_07']
    net_cash_position['net_cash_m8'] = net_cash_position['net_cash_m7'] + net_profit['m_08']
    net_cash_position['net_cash_m9'] = net_cash_position['net_cash_m8'] + net_profit['m_09']
    net_cash_position['net_cash_m10'] = net_cash_position['net_cash_m9'] + net_profit['m_10']
    net_cash_position['net_cash_m11'] = net_cash_position['net_cash_m10'] + net_profit['m_11']
    net_cash_position['net_cash_m12'] = net_cash_position['net_cash_m11'] + net_profit['m_12']
    # Yr2
    net_cash_position['net_cash_m13'] = net_cash_position['net_cash_m12'] + net_profit['m_13']
    net_cash_position['net_cash_m14'] = net_cash_position['net_cash_m13'] + net_profit['m_14']
    net_cash_position['net_cash_m15'] = net_cash_position['net_cash_m14'] + net_profit['m_15']
    net_cash_position['net_cash_m16'] = net_cash_position['net_cash_m15'] + net_profit['m_16']
    net_cash_position['net_cash_m17'] = net_cash_position['net_cash_m16'] + net_profit['m_17']
    net_cash_position['net_cash_m18'] = net_cash_position['net_cash_m17'] + net_profit['m_18']
    net_cash_position['net_cash_m19'] = net_cash_position['net_cash_m18'] + net_profit['m_19']
    net_cash_position['net_cash_m20'] = net_cash_position['net_cash_m19'] + net_profit['m_20']
    net_cash_position['net_cash_m21'] = net_cash_position['net_cash_m20'] + net_profit['m_21']
    net_cash_position['net_cash_m22'] = net_cash_position['net_cash_m21'] + net_profit['m_22']
    net_cash_position['net_cash_m23'] = net_cash_position['net_cash_m22'] + net_profit['m_23']
    net_cash_position['net_cash_m24'] = net_cash_position['net_cash_m23'] + net_profit['m_24']
    # YR2
    net_cash_position['net_cash_m25'] = net_cash_position['net_cash_m24'] + net_profit['m_25']
    net_cash_position['net_cash_m26'] = net_cash_position['net_cash_m25'] + net_profit['m_26']
    net_cash_position['net_cash_m27'] = net_cash_position['net_cash_m26'] + net_profit['m_27']
    net_cash_position['net_cash_m28'] = net_cash_position['net_cash_m27'] + net_profit['m_28']
    net_cash_position['net_cash_m29'] = net_cash_position['net_cash_m28'] + net_profit['m_29']
    net_cash_position['net_cash_m30'] = net_cash_position['net_cash_m29'] + net_profit['m_30']
    net_cash_position['net_cash_m31'] = net_cash_position['net_cash_m30'] + net_profit['m_31']
    net_cash_position['net_cash_m32'] = net_cash_position['net_cash_m31'] + net_profit['m_32']
    net_cash_position['net_cash_m33'] = net_cash_position['net_cash_m32'] + net_profit['m_33']
    net_cash_position['net_cash_m34'] = net_cash_position['net_cash_m33'] + net_profit['m_34']
    net_cash_position['net_cash_m35'] = net_cash_position['net_cash_m34'] + net_profit['m_35']
    net_cash_position['net_cash_m36'] = net_cash_position['net_cash_m35'] + net_profit['m_36']
    computation = merge_two_dicts(computation, net_cash_position)

    #=============#
    # SAVING DATA #
    #=============#
    answer.content = computation
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
