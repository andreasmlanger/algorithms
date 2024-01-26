"""
Overview of different sorting and search algorithms with their respective running times
https://www.bigocheatsheet.com/
"""


import random
import sys
import time

# random numbers will be between 0 and LENGTH * FACTOR
LENGTH = 5000
FACTOR = 10


def print_first_20_numbers(array):
    for i in range(20):
        print(f'{array[i]}, ', end='')
    print('...')


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        rv = func(*args, **kwargs)
        total = time.time() - start
        if isinstance(rv, list):
            print_first_20_numbers(rv)
        else:
            if rv[0] is not None:
                print('\033[36m' + str(rv[1]) + ' was found at position ' + str(rv[0]) + '.')
            else:
                print('\033[91m' + str(rv[1]) + ' was not found.')
        if total > 1:
            print('\033[92m' + str(round(total, 3)) + ' seconds - ', end='')
        else:
            print('\033[92m' + str(round(1000 * total, 2)) + ' milliseconds - ', end='')
        print(func.__name__ + ' \033[36m')
        return rv
    return wrapper


class Random:
    def __init__(self):
        prompt = 'How many numbers would you like to sort? (Default: ' + '\033[92m' + str(LENGTH) + '\033[38m) '
        try:
            self.length = int(input(prompt))
        except ValueError:
            self.length = LENGTH
        self.numbers = [random.randint(0, self.length * FACTOR) for _ in range(self.length)]
        print_first_20_numbers(self.numbers)
        print('\033[36m')


class SortingAlgorithms:
    @timer
    def insert_sort(self, numbers):
        for i in range(1, len(numbers)):
            for j in range(0, i):
                if numbers[j] > numbers[i]:
                    numbers[i], numbers[j] = numbers[j], numbers[i]
        return numbers

    @timer
    def max_sort(self, numbers):
        for i in range(0, len(numbers)):
            for j in range(i, len(numbers)):
                if numbers[j] < numbers[i]:
                    numbers[i], numbers[j] = numbers[j], numbers[i]
        return numbers

    @timer
    def counting_sort(self, numbers):  # O(n + k)
        counters = []
        for i in range(0, max(numbers) + 1):
            counters.append(0)
        for i in range(len(numbers)):
            counters[numbers[i]] += 1
        j = 0
        for i in range(len(counters)):
            while counters[i] > 0:
                numbers[j] = i
                counters[i] -= 1
                j += 1
        return numbers

    @timer
    def radix_sort(self, numbers):  # O(n)
        max1 = max(numbers)  # Find the maximum number to know number of digits
        exp = 1
        b = len(numbers)
        while max1 // exp > 0:
            self.counting_sort_for_radix(exp, numbers, b)
            exp *= b
        return numbers

    @staticmethod
    def counting_sort_for_radix(exp1, numbers, b):
        output = [0] * len(numbers)  # Initialize output array that will have sorted numbers
        count = [0] * b  # Initialize count array as 0
        for i in range(len(numbers)):  # Store count of occurrences in count[]
            index = numbers[i] // exp1
            count[index % b] += 1
        for i in range(1, b):
            count[i] += count[i - 1]
        for i in range(len(numbers) - 1, -1, -1):
            index = numbers[i] // exp1
            output[count[index % b] - 1] = numbers[i]
            count[index % b] -= 1
        for i in range(len(numbers)):  # Copy the output array to arr[], so that arr now contains sorted numbers
            numbers[i] = output[i]

    @timer
    def heap_sort(self, numbers):
        n = len(numbers)
        for i in range(n // 2 - 1, -1, -1):  # Build max-heap, starting at last parent
            self.heapify(numbers, n, i)
        for i in range(n - 1, 0, -1):  # Extract elements one by one
            numbers[i], numbers[0] = numbers[0], numbers[i]  # Swap
            self.heapify(numbers, i, 0)
        return numbers

    def heapify(self, arr, n, i):  # Heapify subtree rooted at index i
        largest = i  # Initialize largest as root
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[i] < arr[left]:  # See if left child of root exists and is greater than root
            largest = left
        if right < n and arr[largest] < arr[right]:  # See if right child of root exists and is greater than root
            largest = right
        if largest != i:  # Change root, if needed
            arr[i], arr[largest] = arr[largest], arr[i]  # Swap
            self.heapify(arr, n, largest)  # Heapify the root

    @timer
    def merge_sort(self, numbers):
        self.merge_sort_step(numbers, 0, len(numbers) - 1)
        return numbers

    def merge_sort_step(self, numbers, left, right):
        if left < right:
            q = (left + right) // 2
            self.merge_sort_step(numbers, left, q)
            self.merge_sort_step(numbers, q + 1, right)

            merge_list = []
            for i in range(q - left + 1):
                merge_list.append(numbers[left + i])
            for i in range(q - left, right - left):
                merge_list.append(numbers[right + q - left - i])
            i = 0
            j = right - left
            for k in range(left, right + 1):
                if merge_list[i] <= merge_list[j]:
                    numbers[k] = merge_list[i]
                    i += 1
                else:
                    numbers[k] = merge_list[j]
                    j -= 1
        return numbers

    @timer
    def quick_sort(self, numbers):
        self.quick_sort_step(numbers, 0, len(numbers) - 1)
        return numbers

    def quick_sort_step(self, numbers, left, right):
        if left < right:
            q = self.partition(numbers, left, right)
            self.quick_sort_step(numbers, left, q)
            self.quick_sort_step(numbers, q + 1, right)
        return numbers

    @staticmethod
    def partition(numbers, left, right):
        x = numbers[(left + right) // 2]
        i = left - 1
        j = right + 1
        while i < j:
            while True:
                i += 1
                if numbers[i] >= x:
                    break
            while True:
                j -= 1
                if numbers[j] <= x:
                    break
            if i < j:
                numbers[i], numbers[j] = numbers[j], numbers[i]
            else:
                return j
        return -1


class SearchAlgorithms:
    def __init__(self, numbers):
        self.numbers = numbers
        prompt = '\033[38m' + '\nWhat number would you like to search? '
        self.n = input(prompt)
        if self.n == '':
            sys.exit()
        while not self.n.isnumeric():
            self.n = input(prompt)
            if self.n == '':
                sys.exit()
        self.n = int(self.n)

    @timer
    def linear_search(self):
        for i in range(len(self.numbers)):
            if self.numbers[i] == self.n:
                print(i + 1, self.n)
                return i + 1, self.n
        return None, self.n

    @timer
    def binary_search(self):
        return self.binary_search_step(self.n, self.numbers, 0, len(self.numbers) - 1), self.n

    def binary_search_step(self, n, numbers, left, right):
        if left > right:
            return
        q = (left + right) // 2
        if n < numbers[q]:
            pos = self.binary_search_step(n, numbers, left, q - 1)
        elif n > numbers[q]:
            pos = self.binary_search_step(n, numbers, q + 1, right)
        else:
            pos = q + 1
        return pos


def main():
    numbers = Random().numbers
    SortingAlgorithms().counting_sort(numbers[:])
    SortingAlgorithms().radix_sort(numbers[:])
    SortingAlgorithms().quick_sort(numbers[:])
    SortingAlgorithms().merge_sort(numbers[:])
    SortingAlgorithms().heap_sort(numbers[:])
    SortingAlgorithms().max_sort(numbers[:])
    SortingAlgorithms().insert_sort(numbers[:])
    while True:
        search = SearchAlgorithms(numbers)
        search.linear_search()
        search.binary_search()


if __name__ == '__main__':
    main()
