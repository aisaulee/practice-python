
with open('myfile.txt', 'w') as f:
    f.write("First line\n")

with open('myfile', 'a') as f:
    f.write("Second line added with 'a' mode\n")