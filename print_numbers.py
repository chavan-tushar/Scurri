'''
This file will print numbers 1-100.
if the number is multiple of 3 then "Three" will be displayed
if the number is multiple of 5 then "Five" will be displayed.
if the number is multiple of 3 and 5 both then "ThreeFive" will be displayed.
else that particular number will be displayed.
'''


def check_if_multiple(n, x):
    return n % x == 0


def print_numbers(n):
    for num in range(1, n + 1):
        to_return = ''
        if check_if_multiple(num, 3):
            to_return += 'Three'
        if check_if_multiple(num, 5):
            to_return += 'Five'
        if not to_return:
            to_return = str(num)
        yield to_return


if __name__ == "__main__":
    n = 100
    for i in print_numbers(n):
        print(i)