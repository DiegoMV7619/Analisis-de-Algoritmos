import random

def create_sorted_array(array_size):
    numbers = random.sample(range(1, (array_size + 1)*10), array_size)
    numbers.sort()
    return numbers

def create_unsorted_array(array_size):
    numbers = random.sample(range(1, (array_size + 1)*10), array_size)
    return numbers

def linear_search(array, number):
    value_found = 0
    for i in range(len(array)):
        if number == array[i]:
            value_found = 1
            break
    return value_found

def binary_search(array, number):
    value_found = 0
    i = 0
    j = len(array) - 1
    while i <= j:
        midpoint = int((i + j)/2)
        if array[midpoint] == number:
            value_found = 1
            return value_found
        
        if number < array[midpoint]:
            j = midpoint - 1
        else:
            i = midpoint + 1
    
    return value_found