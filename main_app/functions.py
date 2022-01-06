def get_mean(evaluate_dict, total_of_participant):
    output = 0.0
    ctr = 4
    for value in evaluate_dict.values():
        if value != 0:
            output += value * ctr
        ctr = ctr - 1
    return output / total_of_participant

def get_facilitator_rate(response_dictionary,get_q9,facilitator_id, data, key):
    response_dictionary[facilitator_id] = {
        "q9":{"4":key,"3":data,"2":0,"1":0},
    }
    for key1, value1 in response_dictionary.items():
        for key2 in value1.keys():
            if key == key1:
                if key2 == data:
                    response_dictionary[facilitator_id][key1][key2] += 1




