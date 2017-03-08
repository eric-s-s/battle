import random as rnd


def random_list(list_len):
    list_of_random_numbers = []
    for _ in range(list_len):
        list_of_random_numbers.append(rnd.random())
    return list_of_random_numbers