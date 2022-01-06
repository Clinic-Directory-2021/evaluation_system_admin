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
    output = 1/2
    response_dictionary[facilitator_id][key][data] += math.floor(output)



