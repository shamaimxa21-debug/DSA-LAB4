"""
CS200L Data Structures and Algorithms (Pr) - Lab 4
Part 3: Sorting Algorithms - Counting Sort, Radix Sort, Bucket Sort (Linear Time Sorting)

Name: Shamaim
Registration No: 2025-GA-112
"""


# ---------------------------------------------------------------
# PART 3a: COUNTING SORT (works with negative numbers too)
# ---------------------------------------------------------------
def counting_sort(arr):
    if not arr:
        return []

    # Negative numbers ke liye: sab values ko min ke hisaab se shift karte hain
    # taake index hamesha 0 se start ho.
    min_val = min(arr)
    max_val = max(arr)
    k = max_val - min_val                 # range of elements

    count = [0] * (k + 1)                 # count array of k+1 zeros
    output = [0] * len(arr)               # output array, same length

    # Step 1: har key ki frequency count karo
    for num in arr:
        count[num - min_val] += 1

    # Step 2: prefix sum -> count[i] = number of elements <= i
    for i in range(1, k + 1):
        count[i] += count[i - 1]

    # Step 3: peeche se traverse karo (stable sort ke liye)
    for i in range(len(arr) - 1, -1, -1):
        j = arr[i] - min_val
        count[j] -= 1
        output[count[j]] = arr[i]

    return output


# ---------------------------------------------------------------
# PART 3b: RADIX SORT (LSD, uses counting sort on each digit)
# ---------------------------------------------------------------
def counting_sort_by_digit(arr, exp):
    """Stable counting sort on the digit at place value `exp` (1, 10, 100...)."""
    n = len(arr)
    output = [0] * n
    count = [0] * 10                      # digits 0-9

    for num in arr:
        digit = (num // exp) % 10
        count[digit] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        count[digit] -= 1
        output[count[digit]] = arr[i]

    return output


def radix_sort(arr):
    if not arr:
        return []
    result = arr[:]
    max_val = max(result)
    exp = 1                               # least significant digit first
    while max_val // exp > 0:
        result = counting_sort_by_digit(result, exp)
        exp *= 10                         # next digit
    return result


# ---------------------------------------------------------------
# PART 3c: BUCKET SORT (for floats uniformly distributed in [0, 1))
# ---------------------------------------------------------------
def insertion_sort(bucket):
    for i in range(1, len(bucket)):
        key = bucket[i]
        j = i - 1
        while j >= 0 and bucket[j] > key:
            bucket[j + 1] = bucket[j]
            j -= 1
        bucket[j + 1] = key
    return bucket


def bucket_sort(arr):
    n = len(arr)
    if n == 0:
        return []

    # 1) n empty buckets banao
    buckets = [[] for _ in range(n)]

    # 2) har element ko bucket[int(n * arr[i])] mein daalo
    for x in arr:
        index = int(n * x)
        buckets[index].append(x)

    # 3) har bucket ko insertion sort se sort karo
    for b in buckets:
        insertion_sort(b)

    # 4) saare buckets ko jod do (concatenate)
    result = []
    for b in buckets:
        result.extend(b)
    return result


# ---------------------------------------------------------------
# MAIN: run all the exercises from the manual
# ---------------------------------------------------------------
if __name__ == "__main__":
    print("\n=== Part 3: Exercise 1 - Counting Sort ===")
    arr1 = [-5, -10, 0, -3, 8, 5, -1, 10]
    print("Input :", arr1)
    print("Output:", counting_sort(arr1))
    # Expected: [-10, -5, -3, -1, 0, 5, 8, 10]

    print("\n=== Part 3: Exercise 2 - Radix Sort ===")
    arr2 = [110, 45, 65, 50, 90, 602, 24, 2, 66]
    print("Input :", arr2)
    print("Output:", radix_sort(arr2))
    # Expected: [2, 24, 45, 50, 65, 66, 90, 110, 602]

    print("\n=== Part 3: Exercise 3 - Bucket Sort ===")
    arr3 = [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434]
    print("Input :", arr3)
    print("Output:", bucket_sort(arr3))
    # Expected: [0.1234, 0.3434, 0.565, 0.656, 0.665, 0.897]
