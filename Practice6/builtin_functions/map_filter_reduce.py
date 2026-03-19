celsius = [-15, 0, 12, 25, 30, 42]
l=filter(lambda x: x>0, celsius)
far=list(map(lambda x: x* 9/5+ 32, l))
print(far)