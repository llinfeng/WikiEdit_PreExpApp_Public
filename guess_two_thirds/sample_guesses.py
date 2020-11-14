import json

# Check 1: that "None" seed does not set the seed
with open('../2019_Data.json', 'r') as f:
    all_guesses = json.loads(f.read())['GS']

import random
random.seed(1)
print(random.sample(all_guesses, 3))
random.seed(1)
print(random.sample(all_guesses, 3))

# Check 2: max in range(0,4)
rand_int_list = []
for elem in range(0,100):

    rand_int_list.append(random.randint(0,4))

print(max(rand_int_list))
print(min(rand_int_list))
