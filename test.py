from field import *

f1: Field = Field([(8, 4), (14, 4)])

unfit = 13
while True:
    unfit = f1.fit("Sixers",unfit)
    if unfit == 0: break;
f1.print()
