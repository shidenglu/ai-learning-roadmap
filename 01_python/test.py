with open("models.txt", "r", encoding="utf-8") as f:
    count = 0
    for line in f:
        count += 1
        print(f"发现模型 ：{line.strip()}")
print(f"总数: {count}\n")