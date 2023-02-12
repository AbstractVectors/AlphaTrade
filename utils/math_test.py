from abstractions import *

std = StandardDeviation(10.0, 100.0, 10.0, 1, 10.0)
print(std.sd)
l = [12.0, 23.0, 23.0, 16.0, 23.0, 21.0, 16.0]
for i in l:
    std.add(i)
    print(std.sd)
std.replace(18.0, 12.0)
std.replace(15.0, 23.0)
print(std.sd)