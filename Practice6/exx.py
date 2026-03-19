numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
newn=[f"even: {x}" if x%2==0 else f"odd: {x}" for x in numbers]
print(newn)