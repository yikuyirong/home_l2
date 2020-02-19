class Student(object):

    def __init__(self, name, gender):
        self.__name = name
        self.__gender = gender

    def get_gender(self):
        return self.__gender

    def set_gender(self, value):
        self.__gender = value


bart = Student("yikuyirong", "male")

bart.set_gender("famale")

print(dir(bart))

L = filter(lambda r: not r.startswith("_"), dir(bart))

print(list(L))
