import math
import statistics
import re

from django.http import response


def get_mean(evaluate_dict, total_of_participant):
    output = 0.0
    ctr = 1
    for key,value in evaluate_dict.items():
        if key != 5:
            output += value * ctr
        ctr = ctr + 1
    return output / total_of_participant

def get_facilitator_rate(response_dictionary,facilitator_id, data, key):
        if key == "exist" or key == "facilitator_name" or  key == "topic":
            print()
        else:
            response_dictionary[facilitator_id][key][data] += 1

def get_facilitator_mean(response_dictionary,total_of_participants):
    for key1, data1 in response_dictionary.items():
        for key2, data2 in data1.items():
            output = 0
            for key3, data3 in data2.items():
                if key3 ==  "mean":
                    response_dictionary[key1][key2][key3] = float("{:.2f}".format(output / total_of_participants))
                else:
                    output += (data3 * int(key3))

def facilitator_overall_mean(mean_dictionary,response_dictionary):
    my_list = []
    for key1, data1 in response_dictionary.items():
            for key2, data2 in data1.items():
                for key3, data3 in data2.items():
                    if key3 ==  "mean":
                        my_list.append(data3)
            mean_dictionary[key1] = round(statistics.mean(my_list),1)
            my_list.clear()
                        
def has_numbers(inputString):
    regex = re.compile('[1234567890@_!#$%^&*()<>?/\|}{~:]')
    if(regex.search(inputString) == None):
        return True
    return False

def question_dict(question,question_dict):
    if question ==  "1":
        question_dict["1"] += 1
    elif question == "2":
        question_dict["2"] += 1
    elif question == "3":
        question_dict["3"] += 1
    elif question == "4":
        question_dict["4"] += 1





