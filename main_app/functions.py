import math

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

def get_facilitator_mean(response_dictionary,mean_dictionary,total_of_participants):
    for key1,value1 in response_dictionary.items():
        for key2,value2 in value1.items():
            mean_dictionary[key1][key2] += value2   



