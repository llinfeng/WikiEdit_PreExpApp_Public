import json
import random

with open("2019_Data.json", "r") as f:
    TR_list = json.loads(f.read())['TR']

random.seed('kk')
random_index = random.choice(range(0,len(TR_list)))
print(TR_list[random_index])



print(len(TR_list))
print(
        max(range(0,
    len(TR_list))))
