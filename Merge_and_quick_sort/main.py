def quicksort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]

    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quicksort(left) + middle + quicksort(right)

def mergesort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        mergesort(left_half)
        mergesort(right_half)

        merge(arr, left_half, right_half)
    return arr

def merge(arr, left_half, right_half):
    i = j = k = 0

    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]:
            arr[k] = left_half[i]
            i += 1
        else:
            arr[k] = right_half[j]
            j += 1
        k += 1

    while i < len(left_half):
        arr[k] = left_half[i]
        i += 1
        k += 1

    while j < len(right_half):
        arr[k] = right_half[j]
        j += 1
        k += 1

def main():
    arreglo1 = [7, 38, 29, 10, 5, 127, 32, 57]
    arreglo2 = [4, 58, 129, 3, 66, 16, 22, 23, 1]
    arreglo_merge = mergesort(arreglo1)
    arreglo_quick = quicksort(arreglo2)
    print("Arreglo ordenado mergesort: ", arreglo_merge)
    print("Arreglo ordenado quicksort: ", arreglo_quick)


if __name__ == "__main__":
    main()