def func1():
    print "world function"

class MyClass(object):
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def hello(self):
        print("and I say hello ({} {} {} and {})".format(self.w, self.x, self.y, self.z))

    def not_hello(self):
        print("You say goodbye ({} {} {} and {})".format(self.w, self.x, self.y, self.z))

if __name__ == '__main__':
    print "world main"

    print("Hello Goodbye, circa  1967")
    song = MyClass("John", "Paul", "George", "Ringo")
    song.not_hello()
    song.hello()
    print("Hello, Hello")




