# import types
from partial import _, __, ___


test_case = [
    {
        "title": "flatten1",
        "method": _.flatten,
        "args": [ [1, [2], [3, [[4]]]] ],
        "expect": [1, 2, 3, 4]
    },
    {
        "title": "flatten2",
        "method": _.flatten,
        "args": [ [1, [2], [3, [[4]]]], True ],
        "expect": [1, 2, 3, [[4]]]
    },
    {
        "title": "difference",
        "method": _.difference,
        "args": [ [1, 2, 3, 4, 5], [5, 2, 10] ],
        "expect": [1, 3, 4]
    },
    {
        "title": "without",
        "method": _.without,
        "args": [ [1, 2, 1, 0, 3, 1, 4], 0, 1 ],
        "expect": [2, 3, 4]
    },
    {
        "title": "union",
        "method": _.union,
        "args": [ [1, 2, 3], [101, 2, 1, 10], [2, 1] ],
        "expect": [1, 2, 3, 101, 10]
    },
    {
        "title": "intersection",
        "method": _.intersection,
        "args": [ [1, 2, 3], [101, 2, 1, 10], [2, 1] ],
        "expect": [1, 2]
    },
    {
        "title": "uniq1",
        "method": _.uniq,
        "args": [ [1, 2, 1, 4, 1, 3] ],
        "expect": [1, 2, 4, 3]
    },
    {
        "title": "uniq2",
        "method": _.uniq,
        "args": [ [1, 2, 1, 4, 1, 3], lambda v, *rest: v % 2 ],
        "expect": [1, 2]
    },
    {
        "title": "zip1",
        "method": _.zip,
        "args": [ ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False] ],
        "expect": [["moe", 30, True], ["larry", 40, False], ["curly", 50, False]]
    },
    # {
    #     "title": "zip2",
    #     "method": _.zip,
    #     "args": [ ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False], ['KKK'] ],
    #     "expect": [["moe", 30, True, "KKK"], ["larry", 40, False, None], ["curly", 50, False, None]]
    # },
    {
        "title": "unzip1",
        "method": _.unzip,
        "args": [ [["moe", 30, True], ["larry", 40, False], ["curly", 50, False]] ],
        "expect": [['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]]
    },
    {
        "title": "unzip2",
        "method": _.unzip,
        "args": [ [["moe", 30, True], ["larry", 40, False], ["curly", 50, False, "KKK"]] ],
        "expect": [['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False], [None, None, 'KKK']]
    },
    {
        "title": "max1",
        "method": _.max,
        "args": [ [1,2,3,4,5] ],
        "expect": 5
    },
    {
        "title": "max2",
        "method": _.max,
        "args": [ [{'name': 'moe', 'age': 40}, {'name': 'larry', 'age': 50}, {'name': 'curly', 'age': 60}], lambda v, *r: v['age'] ],
        "expect": {'name': 'curly', 'age': 60}
    }
]


def test(cases):
    for case in cases:
        if case["method"](*case["args"]) == case["expect"]:
            print("%-13s: PASS" % case["title"])
        else:
            print("%-13s: FAIL" % case["title"])
            print("## expect:", case["expect"], "/ result:", case["method"](*case["args"]), "##")


test(test_case)