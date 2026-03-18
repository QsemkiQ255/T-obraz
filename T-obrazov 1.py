x, y = map(int, input().split())
z = 0
i = 1
g = 1
bill = True
while g < y:
    if g >= x:
        bill = False
        print(g, end=" ")
    z = g
    g += i
    i = z
if bill == True:
    print("В заданном диапазоне нет чисел Фибоначчи")