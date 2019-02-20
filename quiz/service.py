import json

from users.models import Profile


def get_constant(indicator_value):
    """
    Return constant for wrong indicator
    indicator is wrong when it is < 0 or > 100
    Example:
    indicator = -12
    if indicator < 0 then return abs(indicator_value)
    indicator + abs(min_indicator) = 0
    indicator = 105
    if indicator > 100 then return -(indicator % 100)
    -(indicator % 100) = 5
    indicator + -(indicator % 100) = 100
    :param int|float indicator_value: Indicator`s wrong value
    :return: int|float Constant for wrong indicator
    """
    if indicator_value < 0:
        return abs(indicator_value)
    return -(indicator_value % 100)


def check_group_indicators(group_indicator):
    """Return dictionary with correct indicators
    by adding constant
    if indicator is < 0 then constant is positive number
    and by adding constant this indicator become 0
    if is indicator is > 100 then constant is negative number
    and by adding constant this indicator become 100
    :param dict group_indicator: Dictionary with group indicators
    :return:dict Dictionary with correct indicators
    """
    for indicator in group_indicator:
        if not 0 < group_indicator[indicator] < 100:
            group_indicator[indicator] += get_constant(
                group_indicator[indicator])
    return group_indicator


def get_average_results(list_of_answer):
    """
    Return list of average for each answer
    each element in this list is average value for list inside list_of_answer
    :param list list_of_answer: List with lists of users answers
    :return: list List of average result for each answer
    """
    number_of_questions = 24
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
            json.loads(result.user.results_set.last().result))

    return list_of_results


def get_final_result(data, *args):
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
    if isinstance(data, Profile):
        group_answers = [json.loads(
            data.user.results_set.filter(pk=args[0]).first().result)]
    else:
        users_results = data.user.exclude(user__results=None)
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
    average_result = get_average_results(group_answers)
    indicator_list = get_indicators_values(average_result)
    data = check_group_indicators(indicator_list)

    return data
