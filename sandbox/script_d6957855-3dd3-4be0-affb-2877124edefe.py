import time
start = time.time()
for _ in range(10**8): pass
print("Time taken:", time.time() - start)