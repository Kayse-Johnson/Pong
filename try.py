import os
# a = (2,3)
# b = (1,2)
# d = (5,6)
# c = zip(a,b,d)
# # print(tuple(x*y for x,y in zip(a,b)))
# c = list(c)
# print(c)
# d = tuple(c)
# print(d)
a = [1,2]
a.append(5)
print(a)
b = 'le'
c  = 'f'
for letter in b:
    print(letter)

for letter in c:
    print(letter)

print(len(os.listdir(r"C:\Users\Kayse\Games\FlappyBird\flappy-bird-assets\Highscore"))==0)