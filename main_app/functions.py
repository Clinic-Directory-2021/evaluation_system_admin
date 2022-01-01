def get_mean(evaluate_dict, total_of_participant):
    temp = 0
    ctr = 4
    for value in evaluate_dict.values():
        if value != 0:
            temp += value * ctr
        ctr = ctr - 1
    output = temp / total_of_participant 
    return output
