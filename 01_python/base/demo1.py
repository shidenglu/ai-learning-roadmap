import json

class Student:

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def to_dict(self):
        return {
            "name": self.name,
            "score": self.score
        }


students = [
    Student("Tom", 90),
    Student("Alice", 95),
    Student("Bob", 88)
]

# 保存到 JSON
data = [s.to_dict() for s in students]

with open("students.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# 读取
with open("students.json", "r", encoding="utf-8") as f:
    result = json.load(f)

print("读取结果：")
for stu in result:
    print(stu["name"], stu["score"])