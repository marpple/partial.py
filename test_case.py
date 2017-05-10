# import types
from partial import _, __, ___


test_case = {
    "flatten1": {
        "method": _.flatten,
        "args": [ [1, [2], [3, [[4]]]] ],
        "expect": [1, 2, 3, 4]
    },
    "flatten2": {
        "method": _.flatten,
        "args": [ [1, [2], [3, [[4]]]], True ],
        "expect": [1, 2, 3, [[4]]]
    },
    "difference": {
        "method": _.difference,
        "args": [ [1, 2, 3, 4, 5], [5, 2, 10] ],
        "expect": [1, 3, 4]
    },
    "without": {
        "method": _.without,
        "args": [ [1, 2, 1, 0, 3, 1, 4], 0, 1 ],
        "expect": [2, 3, 4]
    },
    "union": {
        "method": _.union,
        "args": [ [1, 2, 3], [101, 2, 1, 10], [2, 1] ],
        "expect": [1, 2, 3, 101, 10]
    },
    "intersection": {
        "method": _.intersection,
        "args": [ [1, 2, 3], [101, 2, 1, 10], [2, 1] ],
        "expect": [1, 2]
    },
    "uniq1": {
        "method": _.uniq,
        "args": [ [1, 2, 1, 4, 1, 3] ],
        "expect": [1, 2, 4, 3]
    },
    "uniq2": {
        "method": _.uniq,
        "args": [ [1, 2, 1, 4, 1, 3], lambda v, *rest: v % 2 ],
        "expect": [1, 2]
    },
    "zip1": {
        "method": _.zip,
        "args": [ ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False] ],
        "expect": [["moe", 30, True], ["larry", 40, False], ["curly", 50, False]]
    },
    "zip2": {
        "method": _.zip,
        "args": [ ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False], ['KKK'] ],
        "expect": [["moe", 30, True, "KKK"], ["larry", 40, False, None], ["curly", 50, False, None]]
    },
    "unzip1": {
        "method": _.unzip,
        "args": [ [["moe", 30, True], ["larry", 40, False], ["curly", 50, False]] ],
        "expect": [['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]]
    },
    "unzip2": {
        "method": _.unzip,
        "args": [ [["moe", 30, True], ["larry", 40, False], ["curly", 50, False, "KKK"]] ],
        "expect": [['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False], [None, None, 'KKK']]
    },
    "max1": {
        "method": _.max,
        "args": [ [1,2,3,4,5] ],
        "expect": 5
    },
    "max2": {
        "method": _.max,
        "args": [ [{'name': 'moe', 'age': 40}, {'name': 'larry', 'age': 50}, {'name': 'curly', 'age': 60}], lambda v, *r: v['age'] ],
        "expect": {'name': 'curly', 'age': 60}
    }
}


def test(cases, key=None):
    def _t(method, args, expect, title):
        if method(*args) == expect:
            print("%-13s: PASS" % title)
        else:
            print("%-13s: FAIL" % title)
            print("## expect:", expect, "/ result:", method(*args), "##")

    keys = cases.keys()
    if key and key in keys:
        _t(cases[key]['method'], cases[key]['args'], cases[key]['expect'], key)
        return

    if key and key not in keys:
        print("not found '%s'" % key)
        return

    for key in keys:
        _t(cases[key]['method'], cases[key]['args'], cases[key]['expect'], key)

test(test_case)