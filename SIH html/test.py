import json
f = open('./data/attendance.json')
print(json.loads(f.read()))