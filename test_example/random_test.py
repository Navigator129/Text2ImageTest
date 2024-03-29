import random
import time


for i in range(10):
    timestamp = float(time.time())
    random.seed(timestamp)
    print(random.randint(1, 10))


