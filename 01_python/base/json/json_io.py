import json

data = {
    "name": "Alice",
    "age": 20
}

# 写入 JSON
with open("user.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# 读取 JSON
with open("user.json", "r", encoding="utf-8") as f:
    obj = json.load(f)

print(obj)