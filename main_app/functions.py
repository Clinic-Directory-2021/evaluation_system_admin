def iterate(dictionary):
    new_list = []
    for k, value in dictionary.items():
        temp = [k , value]
        new_list.append(temp)
    return new_list