class Student(object):
    count = 0

    def __init__(self, name):
        self.name = name
        Student.count = Student.count + 1


print([ Student(str(x)).count for x in range(3) ])


