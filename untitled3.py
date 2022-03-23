import numpy as np

x = np.array(([1,2,3],[4,5,6],[7,8,9]))
y = 10*x

for a, b in zip(x,y):
    print(a)