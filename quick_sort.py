def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[-1]

    left = []
    right = []
    equal = []

    for x in arr:
        if x < pivot:
            left.append(x)
        elif x > pivot:
            right.append(x)
        else:
            equal.append(x)

    return quick_sort(left) + equal + quick_sort(right)


arr = [10, 7, 8, 9, 1, 5]

print("Original Array:", arr)
print("Sorted Array:", quick_sort(arr))