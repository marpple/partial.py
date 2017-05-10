# import types
from partial import _, __, ___


test_case = [
    {
        "title": "flatten1",
        "method": _.flatten,
        "args": [[1, [2], [3, [[4]]]]],
        "expect": [1, 2, 3, 4]
    }, {
        "title": "flatten2",
        "method": _.flatten,
        "args": [[1, [2], [3, [[4]]]], True],
        "expect": [1, 2, 3, [[4]]]
    }, {
        "title": "difference",
        "method": _.difference,
        "args": [[1, 2, 3, 4, 5], [5, 2, 10]],
        "expect": [1, 3, 4]
    }, {
        "title": "without",
        "method": _.without,
        "args": [[1, 2, 1, 0, 3, 1, 4], 0, 1],
        "expect": [2, 3, 4]
    }, {
        "title": "union",
        "method": _.union,
        "args": [[1, 2, 3], [101, 2, 1, 10], [2, 1]],
        "expect": [1, 2, 3, 101, 10]
    }, {
        "title": "intersection",
        "method": _.intersection,
        "args": [[1, 2, 3], [101, 2, 1, 10], [2, 1]],
        "expect": [1, 2, 3] #[1, 2]
    }, {
        "title": "uniq",
        "method": _.uniq,
        "args": [[1, 2, 1, 4, 1, 3]],
        "expect": [1, 2, 4, 3]
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