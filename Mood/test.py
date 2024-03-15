import json
with open('./train.json', 'r', encoding="utf8") as file:
    listJson = json.loads(file.read())

numint = 0
numstr = 0
numoth = 0
for i in listJson:
    print(i[0])
    print(i[1])  # Debugging
    if isinstance(i[1], str):
        numstr += 1
    elif isinstance(i[1], int):
        numint += 1
    else:
        numoth += 1


print(f"numstr = {numstr}")
print(f"numint = {numint}")
print(f"numoth = {numoth}")
    
    