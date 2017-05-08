# partial.py
import types

___ = {}


class Partial(object):
    def __init__(self):
        self.VERSION = "0.0.1"

    identity = idtt = lambda self, val, *rest: val

    always = const = lambda self, val, *rest: lambda *args: val

    def is_func(self, val):
        return isinstance(val, types.FunctionType) or callable(val)
    isFunction = is_function = is_func

    def is_dict(self, val):
        return type(val) is dict
    isDictionary = is_dictionary = is_dict

    def is_list(self, val):
        return type(val) is list
    isList = is_list

    def is_tuple(self, val):
        return type(val) is tuple
    isTuple = is_tuple

    def is_list_or_tuple(self, val):
        t = type(val)
        return t is list or t is tuple

    def is_none(self, val):
        return val is None
    isNone = is_none

    def is_mr(self, val):
        return self.is_dict(val) and val.get('_mr')

    def mr(self, *args):
        return {'value': args, '_mr': True}

    def go(self, seed, *funcs):
        seed = seed() if self.is_func(seed) else seed
        for func in funcs:
            seed = func(*seed.get('value')) if self.is_mr(seed) else func(seed)
        return seed

    def pipe(self, *funcs):
        return lambda *seed: self.go(seed[0] if len(seed) == 1 else self.mr(*seed), *funcs)

    def partial(self, func, *parts):
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

            merged = args1 + rest + args2

            return func(*merged)

        return _partial

    def range(self, start, stop=None, step=None):
        if stop is None:
            return list(range(start))
        if step is None:
            return list(range(start, stop))
        return list(range(start, stop, step))

    def each(self, data, iteratee):
        if type(data) is list or type(data) is tuple:
            for i in range(len(data)):
                iteratee(data[i], i, data)
        elif type(data) is dict:
            for k in data.keys():
                iteratee(data[k], k, data)

    def map(self, data, iteratee=None):
        if iteratee is None and self.is_func(data):
            return self.partial(self.map, _, data)
        result = []
        if type(data) is list or type(data) is tuple:
            for i in range(len(data)):
                result.append(iteratee(data[i], i, data))
        elif type(data) is dict:
            for k in data.keys():
                result.append(iteratee(data[k], k, data))
        return result

    def reduce(self, data, iteratee=None, memo=None):
        if self.is_func(data):
            return self.partial(self.reduce, _, data, iteratee)
        if type(data) is list or type(data) is tuple:
            memo = memo if memo else data.pop(0)
            for i in range(len(data)):
                memo = iteratee(memo, data[i], i, data)
        elif type(data) is dict:
            keys = data.keys()
            if memo is None:
                keys = list(keys)
                memo = data[keys.pop(0)]
            for k in keys:
                memo = iteratee(memo, data[k], k, data)
        return memo

    def reduce_right(self, data, iteratee=None, memo=None):
        if self.is_func(data):
            return self.partial(self.reduce_right, _, data, iteratee)
        if type(data) is list or type(data) is tuple:
            memo = memo if memo else data.pop()
            for i in range(len(data)-1, -1, -1):
                memo = iteratee(memo, data[i], i, data)
        elif type(data) is dict:
            keys = list(data.keys())
            keys.reverse()
            if memo is None:
                memo = data[keys.pop(0)]
            for k in keys:
                memo = iteratee(memo, data[k], k, data)
        return memo
    reduceRight = reduce_right

    def find(self, data, predicate=None):
        if predicate is None and self.is_func(data):
            return self.partial(self.find, _, data)
        if type(data) is list or type(data) is tuple:
            for i in range(len(data)):
                if predicate(data[i], i, data):
                    return data[i]
        elif type(data) is dict:
            for k in data.keys():
                if predicate(data[k], k, data):
                    return data[k]
        return None

    def find_i(self, arr, predicate=None):
        if predicate is None and self.is_func(arr):
            return self.partial(self.find_i, _, arr)
        if type(arr) is dict:
            return -1
        for i in range(len(arr)):
            if predicate(arr[i], i, arr):
                return i
        return -1
    findIndex = find_index = find_i

    def find_k(self, obj, predicate):
        if predicate is None and self.is_func(obj):
            return self.partial(self.find_k, _, obj)
        if type(list) is not obj:
            return None
        for k in obj.keys():
            if predicate(obj[k], k, obj):
                return k
        return None
    findKey = find_key = find_k

    def pluck(self, data, key=None):
        if key is None:
            return self.partial(self.pluck, _, data)
        return self.map(data, lambda v, *rest: v[key])

    def filter(self, data, iteratee=None):
        if iteratee is None and self.is_func(data):
            return self.partial(self.filter, _, data)
        result = []
        if type(data) is list or type(data) is tuple:
            for i in range(len(data)):
                if iteratee(data[i], i, data):
                    result.append(data[i])
        elif type(data) is dict:
            for k in data.keys():
                if iteratee(data[k], k, data):
                    result.append(data[k])
        return result

    def reject(self, data, iteratee=None):
        if iteratee is None and self.is_func(data):
            return self.partial(self.reject, _, data)

        return self.filter(data, self.negate(iteratee))

    def negate(self, predicate):
        return lambda *args: not predicate(*args)

    def first(self, arr, num=1):
        return arr[0:num]
    head = take = first

    def last(self, arr, num=1):
        return arr[-num]

    def initial(self, arr, num=1):
        if num is 0:
            return arr[0:]
        else:
            return arr[0:-num]

    def rest(self, arr, num=1):
        return arr[num:len(arr)]
    tail = drop = rest

    def compact(self, arr):
        return self.filter(arr, self.idtt)

    def flatten(self, arr, shallow=False):
        res = []

        def _flat(value):
            for val in value:
                if not self.is_list_or_tuple(val):
                    res.append(val)
                elif shallow:
                    self.each(val, lambda v, *rest: res.append(v))
                else:
                    _flat(val)
        _flat(arr)
        return res

    def difference(self, arr, values):
        res = []
        for v in arr:
            if v not in values:
                res.append(v)
        return res

    def without(self, arr, *values):
        return self.difference(arr, values)

    def union(self, *arrays):
        res = []
        for arr in arrays:
            for v in arr:
                if v not in res:
                    res.append(v)
        return res

    def intersection(self, *arrays):
        res, ran, flag = ([], range(len(arrays)), False)
        for arr in arrays:
            for v in arr:
                for i in ran:
                    flag = True if v in arrays[i] else False
                if flag and v not in res:
                    res.append(v)
                flag = False
        return res

    def uniq(self, arr, isSorted=False, iteratee=None):
        res = []
        for v in arr:
            if v not in res:
                res.append(v)
        return res
    unique = uniq


_ = Partial()
__ = _.pipe