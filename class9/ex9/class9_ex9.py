#!/usr/bin/env python
"""
9. Write a Python script in a different directory (not the one containing mytest).

    a. Verify that you can import mytest and call the three functions func1(), func2(), and func3().
    b. Create an object that uses MyClass. Verify that you call the hello() and not_hello() methods.
"""

from mytest import func1, func2, func3, MyClass


__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

def main():
    func1()
    func2()
    func3()

    song = MyClass('John', 'Paul', 'George', 'Ringo')
    song.not_hello()
    song.hello()

if __name__ == "__main__":
    main()