celsius = [-15, 0, 12, 25, 30, 42]
l=filter(lambda x: x>0, celsius)
far=list(map(lambda x: x* 9/5+ 32, l))
print(far)

from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

squared = list(map(lambda x: x**2, numbers))

evens = list(filter(lambda x: x % 2 == 0, numbers))

product = reduce(lambda x, y: x * y, numbers)

print(f"Квадраты: {squared}\nЧетные: {evens}\nПроизведение: {product}")