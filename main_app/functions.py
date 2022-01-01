def iterate(dictionary):
    new_list = []
    for key, value in dictionary.iteritems():
        temp = [key,value]
        new_list.append(temp)
    return new_list