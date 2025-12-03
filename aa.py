import json

print("Loading json...")
with open("methods.json", "r") as f:
    file = json.load(f)

count = 0
for i in range(16777216):
    if i % 100000 == 0: print(i)
    if file[str(i)] != 0: count += 1

print(count)
