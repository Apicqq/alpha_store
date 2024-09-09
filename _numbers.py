def print_numbers(num: int) -> str:
    return "".join([str(number) * number for number in range(1, num + 1)])


print(print_numbers(3))

print(print_numbers(55))