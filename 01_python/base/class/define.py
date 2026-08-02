class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"我是{self.name}，今年{self.age}岁")

p = Person("Alice", 20)

print(p.name)
p.introduce()

class Student(Person):

    def __init__(self, name, age, school):
        super().__init__(name, age)
        self.school = school

    def study(self):
        print(f"{self.name} 在学习")

s = Student("Tom", 18, "NTU")

s.introduce()
s.study()

class User:

    count = 0

    def __init__(self, name):
        self.name = name
        User.count += 1

u1 = User("A")
u2 = User("B")

print(User.count)