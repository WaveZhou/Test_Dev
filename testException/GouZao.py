class Person(object):
    def __int__(self):
        print("hahaha")

    def __init__(self, age, name):
        self.age = age
        self.name = name

    def print_person(self):
        print(self.age, self.name)
    def __str__(self):
        return str(self.age + self.name)
   # def __repr__(self):
        return 'hhhh' + str(self.age + self.name)
if __name__ == '__main__':
    p = Person(46,56)
    print(p)
