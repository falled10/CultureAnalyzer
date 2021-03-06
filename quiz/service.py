import json

from django.contrib.auth import get_user_model

__all__ = ['check_group_indicators', 'get_average_results',
           'get_indicators_values', 'get_groups_results',
           'get_final_buisness_result',
           'NUMBER_OF_QUESTION_FOR_BUSINESS_QUIZ',
           'MAX_INDICATOR_VALUE', 'MIN_INDICATOR_VALUE']

NUMBER_OF_QUESTION_FOR_BUSINESS_QUIZ = 24

MIN_INDICATOR_VALUE = 0
MAX_INDICATOR_VALUE = 100


def check_group_indicators(group_indicator):
    """Return dictionary with correct indicators
    by adding constant
    if indicator is < 0 then shift value of indicator to 0
    if is indicator is > 100 then shift value of indicator to 100
    :param dict group_indicator: Dictionary with group indicators
    :return:dict Dictionary with correct indicators
    """
    for indicator in group_indicator:
        if group_indicator[indicator] < MIN_INDICATOR_VALUE:
            group_indicator[indicator] = MIN_INDICATOR_VALUE
        elif group_indicator[indicator] > MAX_INDICATOR_VALUE:
            group_indicator[indicator] = MAX_INDICATOR_VALUE
    return group_indicator


def get_average_results(list_of_answer, number_of_questions):
    """
    Return list of average for each answer
    each element in this list is average value for list inside list_of_answer
    :param int number_of_questions: number of questions in quiz
    :param list list_of_answer: List with lists of users answers
    :return: list List of average result for each answer
    """
    avg_list = []
    for i in range(number_of_questions):
        avg_list.append(sum([result[i] for result in list_of_answer]) / len(
            list_of_answer))
    return avg_list


def get_indicators_values(answers_list):
    """
    Return value for each indicator by formulas
    :return: dict dictionary with value for each indicator
    """
    group = {'pdi': round(35 * (answers_list[6] - answers_list[1]) + 25 * (
            answers_list[19] - answers_list[22]), 2),
             'idv': round(35 * (answers_list[3] - answers_list[0]) + 35 * (
                     answers_list[8] - answers_list[5]), 2),
             'mas': round(35 * (answers_list[4] - answers_list[2]) + 35 * (
                     answers_list[7] - answers_list[9]), 2),
             'uai': round(40 * (answers_list[17] - answers_list[14]) + 25 * (
                     answers_list[20] - answers_list[23]), 2),
             'lto': round(40 * (answers_list[12] - answers_list[13]) + 25 * (
                     answers_list[18] - answers_list[21]), 2),
             'ivr': round(35 * (answers_list[11] - answers_list[10]) + 40 * (
                     answers_list[16] - answers_list[15]), 2)}
    return group


def get_groups_results(data):
    """
    Return list with list of results

    :param list data: List with users profile
    :return: List with lists of results
    """
    list_of_results = []
    for result in data:
        list_of_results.append(
            json.loads(result.results_set.last().result))

    return list_of_results


def get_final_buisness_result(data, *args):
    """
    Return dictionary of indicators with correct values
    If data is Profile objects then args should be id of result
    If data is Group object then args is not required

    If users in group have not results then return dictionary of indicators
    with 0 values

    :param Profile|Group data:
    :param int args: id of result (only for profile)
    :return dict: Dictionary of indicators
    """
    if isinstance(data, get_user_model()):
        group_answers = [json.loads(
            data.results_set.filter(pk=args[0]).first().result)]
    else:
        users_results = data.user.exclude(results=None)
        if not users_results:
            return {
                'pdi': 0,
                'idv': 0,
                'mas': 0,
                'uai': 0,
                'lto': 0,
                'ivr': 0,
            }
        group_answers = get_groups_results(users_results)
    average_result = get_average_results(group_answers,
                                         NUMBER_OF_QUESTION_FOR_BUSINESS_QUIZ)
    indicator_list = get_indicators_values(average_result)
    data = check_group_indicators(indicator_list)
    return data
