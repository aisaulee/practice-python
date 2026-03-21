names = ["Aisaule", "Askar", "Arman"]
points = [95, 82, 77]
res= zip(names, points)
print(tuple(res))

pro=["Apple", "Milk", "Bread"]
print(list(enumerate(pro)))


names = ["Aisaule", "Arman", "Elena"]
phones = ["77477000000", "77017000000", "77077000000"]

for name, phone in zip(names, phones):
    print(f"Контакт: {name} -> {phone}")

for index, name in enumerate(names, start=1):
    print(f"{index}. {name}")