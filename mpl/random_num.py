# Prepare for rand number generator, a test of what random numbers are we getting
from random import randrange
from random import seed as rand_seed


# Seed
rand_seed(99)
for i in range(100):
    # 0 - 4, inclusive, with ticks at 0.01 (same as the slider outcome)
    rand_num = randrange(0, 400, 1) / 100

    print(rand_num)
