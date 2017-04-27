# from underscore import _



# <Partial.py>
import types


identity = idtt = lambda val: val


always = const = lambda val: lambda: val


def is_func(val):
    return isinstance(val, types.FunctionType)


def is_dict(val):
    return type(val) is dict


def is_mr(val):
    return is_dict(val) and val.get('_mr')


def mr(*args):
    return {'value': args, '_mr': True}


def go(seed, *funcs):
    seed = seed() if is_func(seed) else seed
    for func in funcs:
        seed = func(*seed.get('value')) if is_mr(seed) else func(seed)
    return seed


def pipe(*funcs):
    return lambda *seed: go(seed[0] if len(seed) == 1 else mr(*seed), *funcs)


# def pipe(*funcs):
#     def _pipe(*seed):
#         _seed = seed[0] if len(seed) == 1 else mr(*seed)
#         return go(_seed, *funcs)
#     return _pipe


def partial(func, *parts):
    parts1, parts2, ___idx = ([], [], len(parts))

    for i in range(___idx):
        if parts[i] == ___:
            ___idx = i
        elif i < ___idx:
            parts1.append(parts[i])
        else:
            parts2.append(parts[i])

    def _partial(*args):
        args1, args2, rest = (parts1[:], parts2[:], list(args))

        for j in range(len(args1)):
            if args1[j] == _:
                args1[j] = rest.pop(0)

        for j in range(len(args2)):
            if args2[j] == _:
                args2[j] = rest.pop()

        return func(*args1, *rest, *args2)

    return _partial

_ = partial
___ = {}



# <TEST>

def _sum(*args):
    args = args[0] if len(args) == 1 else args
    sum = 0
    for i in args:
        sum = sum + i
    return sum


def sum10(n):
    return _sum(n, 10)


# res = go(mr(3, 4, 5), _sum, sum10)
# print(res)

# pp = pipe(_sum, sum10)
# print(pp(range(1, 11)))


part1 = partial(print, _, 0, ___, 0, _, 0)
# part2 = partial(print, 10, 20)

part1(111, 222, 333, 444)
# part2(30)


print(always(111)())

# arr = 1,2,3,4
# dic = {'value': arr, '_mr': True}
# dic2 = {'value': arr}
#
# print(is_mr(dic2))
#
# print(is_mr(dic), is_mr(dic2))

# print(type(dic) is dict)

# # while문 테스트
# prompt = """
#     1. Add
#     2. Del
#     3. List
#     4. Quit
#
#     Enter number: """
#
# number = 0
#
# while number != 4:
#     print(prompt)
#     number = int(input())


# # 커피자판기
# coffee = 10
# money = 300
# while money:
#     print("몇 잔의 커피를 원하시나요?")
#     order = int(input())
#     if order < coffee and coffee > 0:
#         coffee = coffee - order
#         print("여기 %d잔의 커피를 드립니다." % order)
#         print("남은 커피의 양은 %d잔 입니다." % coffee)
#     else:
#         print("남은 커피가 %d잔뿐입니다. 남은 커피를 모두 드립니다." % coffee)
#         print("이제 커피가 다 떨어졌습니다. 판매를 종료합니다.")
#         break


# result = [x*y for x in range(2, 10) for y in range(1, 10)]
# print(result)