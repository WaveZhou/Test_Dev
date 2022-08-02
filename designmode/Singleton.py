# 实例化一个单例
class Singleton(object):
    __instance = None

    def __new__(cls, age, name):
        # 如果类数字能够__instance没有或者没有赋值
        # 那么就创建一个对象，并且赋值为这个对象的引用，保证下次调用这个方法时
        # 能够知道之前已经创建过对象了，这样就保证了只有1个对象
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
            cls.__instance.age = age
            cls.__instance.name = name
        return cls.__instance


# a = Singleton(18, "dongGe")
b = Singleton(8, "dongGe")
id()  # 此为查看某个对象的内存位置，是一串数字，数字相同，表示为同一个对象
# print(id(a))
print(id(b))

# a.age = 19  # 给a指向的对象添加一个属性
print(b.age)  # 获取b指向的对象的age属性
