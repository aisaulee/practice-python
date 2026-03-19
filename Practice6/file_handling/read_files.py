with open("myfile.txt", "r") as file:
    print(file.read())

with open("myfile.txt") as f:
  print(f.read(5))

with open("myfile.txt") as f:
  print(f.readline())


with open("myfile.txt") as f:
  for x in f:
    print(x)