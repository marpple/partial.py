import unittest
# from unittesthelper import init
# init()  # will let you import modules from upper folder
from partial import _, __, ___
from threading import Timer


class TestStructure(unittest.TestCase):

    # class Namespace:
    #     pass
    #
    # def test_bind(self):
    #     pass
    #
    # def test_bindAll(self):
    #     pass
    #
    # def test_memoize(self):
    #     def fib(n):
    #         return n if n < 2 else fib(n - 1) + fib(n - 2)
    #
    #     fastFib = _.memoize(fib)
    #     self.assertEqual(
    #         fib(10), 55, 'a memoized version of fibonacci'
    #                      ' produces identical results')
    #     self.assertEqual(
    #         fastFib(10), 55, 'a memoized version of fibonacci'
    #         ' produces identical results')
    #     self.assertEqual(
    #         fastFib(10), 55, 'a memoized version of fibonacci'
    #         ' produces identical results')
    #     self.assertEqual(
    #         fastFib(10), 55, 'a memoized version of fibonacci'
    #         ' produces identical results')
    #
    #     def o(str):
    #         return str
    #
    #     fastO = _.memoize(o)
    #     self.assertEqual(o('upper'), 'upper', 'checks hasOwnProperty')
    #     self.assertEqual(fastO('upper'), 'upper', 'checks hasOwnProperty')
    #
    # def test_delay(self):
    #     abc = False
    #
    #     def func():
    #         nonlocal abc
    #         abc =True
    #
    #     _.delay(func, 150)
    #
    #     def checkFalse():
    #         self.assertFalse(abc)
    #         print("\nASYNC: delay. OK")
    #
    #     def checkTrue():
    #         self.assertTrue(abc)
    #         print("\nASYNC: delay. OK")
    #
    #     Timer(0.05, checkFalse).start()
    #     Timer(0.20, checkTrue).start()
    # #
    # def test_defer(self):
    #     ddd = False
    #
    #     def defertTest(bool):
    #         ddd = bool
    #
    #     _.defer(defertTest, True)
    #
    #     def deferCheck():
    #         self.assertTrue(True, "deferred the function")
    #         print("\nASYNC: defer. OK")
    #
    #     _.delay(deferCheck, 50)
    #
    # def test_throttle(self):
    #     abc = 0
    #
    #     def incr():
    #         nonlocal abc
    #         print(abc)
    #         abc += 1
    #
    #     throttledIncr = _.throttle(incr, 0.1)
    #     throttledIncr()
    #     throttledIncr()
    #     throttledIncr()
    #     Timer(0.07, throttledIncr).start()
    #     Timer(0.12, throttledIncr).start()
    #     Timer(0.14, throttledIncr).start()
    #     Timer(0.19, throttledIncr).start()
    #     Timer(0.22, throttledIncr).start()
    #     Timer(0.34, throttledIncr).start()
    #     #
    #     def checkCounter1():
    #         self.assertEqual(abc, 1, "incr was called immediately")
    #         print("ASYNC: throttle. OK")
    #
    #     def checkCounter2():
    #         self.assertEqual(abc, 4, "incr was throttledfffff")
    #         print("ASYNC: throttle. OK")
    #
    #     _.delay(checkCounter1, 90)
    #     _.delay(checkCounter2, 400)

    # def test_debounce(self):
    #     con = 0
    #
    #     def incr():
    #         nonlocal con
    #         con += 1
    #
    #     debouncedIncr = _.debounce(incr, 120)
    #     debouncedIncr()
    #     debouncedIncr()
    #     debouncedIncr()
    #     Timer(0.03, debouncedIncr).start()
    #     Timer(0.06, debouncedIncr).start()
    #     Timer(0.09, debouncedIncr).start()
    #     Timer(0.12, debouncedIncr).start()
    #     Timer(0.15, debouncedIncr).start()
    #
    #     def checkCounter():
    #         self.assertEqual(1, con, "incr was debounced")
    #         print("ASYNC: debounce. OK")
    #
    #     _.delay(checkCounter, 300)
    #
    def test_once(self):
        con = 0

        def add():
            nonlocal con
            con += 1

        increment = _.once(add)
        increment()
        increment()
        increment()
        increment()
        self.assertEqual(con, 1)
    #
    # def test_wrap(self):
    #     def greet(name):
    #         return "hi: " + name
    #
    #     def wrap(func, name):
    #         aname = list(name)
    #         aname.reverse()
    #         reveresed = "".join(aname)
    #         return func(name) + ' ' + reveresed
    #     backwards = _.wrap(greet, wrap)
    #     self.assertEqual(backwards('moe'), 'hi: moe eom',
    #                      'wrapped the saluation function')
    #
    #     inner = lambda: "Hello "
    #     obj = {"name": "Moe"}
    #     obj["hi"] = _.wrap(inner, lambda fn: fn() + obj["name"])
    #     self.assertEqual(obj["hi"](), "Hello Moe")
    #
    # def test_compose(self):
    #     def greet(name):
    #         return "hi: " + name
    #
    #     def exclaim(sentence):
    #         return sentence + '!'
    #
    #     def upperize(full):
    #         return full.upper()
    #
    #     composed_function = _.compose(exclaim, greet, upperize)
    #
    #     self.assertEqual('HI: MOE!', composed_function('moe'),
    #                      'can compose a function that takes another')
    #
    # def test_after(self):
    #
    #     con = None
    #     def testAfter(afterAmount, timesCalled):
    #         nonlocal con
    #         con = 0
    #
    #         def afterFunc():
    #             nonlocal con
    #             con += 1
    #
    #         after = _.after(afterAmount, afterFunc)
    #
    #         while (timesCalled):
    #             after()
    #             timesCalled -= 1
    #
    #         return con
    #
    #     self.assertEqual(testAfter(5, 5), 1,
    #                      "after(N) should fire after being called N times")
    #     self.assertEqual(testAfter(5, 4), 0,
    #                      "after(N) should not fire unless called N times")
    #     self.assertEqual(testAfter(0, 1), 1,
    #                      "after(0) should fire immediately")
    #

    def test_partial(self):
        func = _.partial(lambda *args: args, _, 10, ___, _, 100, _, 300)
        self.assertEqual((0, 10, 20, 30, 40, 50, 60, 100, 200, 300),
                         func(0, 20, 30, 40, 50, 60, 200), "partial did not work")

if __name__ == "__main__":
    print("run these tests by executing `python -m unittest"
          "discover` in unittests folder")
    unittest.main()