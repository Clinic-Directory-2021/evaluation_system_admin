def get_mean(evaluate_dict, total_of_participant):
    output = 0.0
    ctr = 4
    for value in evaluate_dict.values():
        if value != 0:
            output += value * ctr
        ctr = ctr - 1
    return output / total_of_participant

def get_facilitator_rate(response_dictionary,facilitator_id, data, key):
    
    if key in response_dictionary[facilitator_id].keys():
        if data in response_dictionary[facilitator_id][key].keys():
            response_dictionary[facilitator_id][key][data] += 1
        else:
            response_dictionary[facilitator_id][key][data] = 1
    else:
        if data in response_dictionary[facilitator_id][key].keys():
            response_dictionary[facilitator_id][key][data] += 1
        else:
            response_dictionary[facilitator_id][key][data] = 1




