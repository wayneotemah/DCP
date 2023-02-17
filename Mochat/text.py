import json
now = [(1,2,3)(2,3,6)]
dumped = json.dumps(now)
loaded = json.loads(dumped)
print(type(dumped))
print(type(loaded))
