def get_mean(evaluate_dict, total_of_participant):
    output = 0.0
    ctr = 4
    for value in evaluate_dict.values():
        if value != 0:
            output += value * ctr
        ctr = ctr - 1
    return output / total_of_participant

def get_facilitator_rate(response_dictionary,facilitator_id, data, key):
    response_dictionary[facilitator_id] = {
        "q9":{"4":0,"3":0,"2":0,"1":0},
    }
    response_dictionary["q9"]["4"] = key




