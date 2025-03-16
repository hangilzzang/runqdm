from runqdm import runqdm
import time

for i in runqdm(796):
    sum(x ** 2 for x in range(1, 10**7))  


# print('done')
