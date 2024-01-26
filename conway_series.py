"""
Generator for Conway series
https://en.wikipedia.org/wiki/Look-and-say_sequence
"""

LENGTH = 10


def conway(start, length):
    series = str(start)
    for i in range(length):
        print('{:02}: '.format(i + 1) + series)
        series = conway_count(series)


def conway_count(series):
    i = 0
    string = ''
    while i < len(series):
        digit = series[i]
        counter = 1
        while i + 1 < len(series):
            if series[i] == series[i + 1]:
                counter += 1
                i += 1
            else:
                break
        string += str(counter) + str(digit)
        i += 1
    return string


conway(1, LENGTH)
