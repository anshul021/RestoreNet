import time

start = time.time()
import numpy
count = 0
mean = 0.0
M2 = 0.0
for i in range(1000):
    count += 1
    delta = i - mean
    mean += delta / count
    M2 += delta * (i - mean)

end = time.time()
print(end - start)