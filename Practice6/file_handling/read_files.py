
with open('myfile.txt', 'r') as f:

    for line in f:
        print(line.strip())

with open('myfile.txt', 'r') as f:
    lines = f.readlines()
    print(len(lines))