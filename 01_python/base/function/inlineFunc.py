numbers = [1, 2, 3, 4, 5]

print(len(numbers))
print(max(numbers))
print(min(numbers))
print(sum(numbers))

# map
result = list(map(lambda x: x * 2, numbers))
print(result)

# filter
result = list(filter(lambda x: x % 2 == 0, numbers))
print(result)