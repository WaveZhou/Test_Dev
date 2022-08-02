class A:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def origin(self):
        print("我是你们的爸爸方法")
        #return NotImplemented

    def speak(self):
        print('my name is {}'.format(self.name), 'my age is{}'.format(self.age))


class B(A):
    def __init__(self, name, age):
        super().__init__(name, age)
        self.name = '张思'

    # def origin(self):
    #     return NotImplemented
        #print('我是B的实现')


class C(B):
    def __init__(self, name, age):
        super().__init__(name, age)
        self.name = '张思'

    def origin(self):
        #return NotImplemented
        print('我是C的实现')


b = B('张三', '36')
b.origin()
b = C('李四', '36')
b.origin()
