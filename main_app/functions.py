import math
import statistics

from django.http import response


def get_mean(evaluate_dict, total_of_participant):
    output = 0.0
    ctr = 4
    for value in evaluate_dict.values():
        if value != 0:
            output += value * ctr
        ctr = ctr - 1
    return output / total_of_participant

def get_facilitator_rate(response_dictionary,facilitator_id, data, key):
    response_dictionary[facilitator_id][key][data] += 1/2

def get_facilitator_mean(response_dictionary,total_of_participants):
    for key1, data1 in response_dictionary.items():
        for key2, data2 in data1.items():
            output = 0
            for key3, data3 in data2.items():
                if key3 ==  "mean":
                    response_dictionary[key1][key2][key3] = output / total_of_participants
                else:
                    output += (data3 * int(key3))

def facilitator_overall_mean(mean_dictionary,response_dictionary):
    my_list = []
    for key1, data1 in response_dictionary.items():
            for key2, data2 in data1.items():
                for key3, data3 in data2.items():
                    if key3 ==  "mean":
                        my_list.append[data3]
            mean_dictionary[key1] = statistics.mean(my_list)
            my_list.clear()
                        





