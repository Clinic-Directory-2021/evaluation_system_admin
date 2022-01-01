def get_mean(evaluate_dict, total_of_participant):
    output = 0
    ctr = 4
    for value in evaluate_dict.values():
        if value != 0:
            output += value * ctr
        ctr = ctr - 1
    output = output  
    return output
