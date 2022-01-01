def get_mean(evaluate_dict, total_of_participant):
    output = 0.0
    ctr = 4
    for value in evaluate_dict.values():
        output += value * ctr
        ctr -= 1
    output = output/total_of_participant    
    return output
