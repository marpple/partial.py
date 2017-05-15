# Partial.py 1.0
# Project Lead - Indong Yoo
# Maintainers - Jeongik Park, Joeun Ha
# (c) 2017 Marpple. MIT Licensed.
import types
from threading import Timer

___ = {}


class Partial(object):
    def __init__(self):
        self.VERSION = "1.0"

    # go, pipe, partial
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

    # Collections
    def each(self, data, iter):
        if type(data) is list or type(data) is tuple:
            for i in range(len(data)):
                iter(data[i], i, data)
        elif type(data) is dict:
            for k in data.keys():
                iter(data[k], k, data)
    forEach = each

    def map(self, data, iteratee=None):
        if iteratee is None and self.is_func(data):
            return self.partial(self.map, _, data)
        res = []
        if type(data) is list or type(data) is tuple:
            for i in range(len(data)):
                res.append(iteratee(data[i], i, data))
        elif type(data) is dict:
            for k in data.keys():
                res.append(iteratee(data[k], k, data))
        return res
    collect = map

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
    inject = fold = reduce

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
    foldr = reduceRight = reduce_right

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
    detect = find

    def filter(self, data, predicate=None):
        if predicate is None and self.is_func(data):
            return self.partial(self.filter, _, data)
        res = []
        if type(data) is list or type(data) is tuple:
            for i in range(len(data)):
                if predicate(data[i], i, data):
                    res.append(data[i])
        elif type(data) is dict:
            for k in data.keys():
                if predicate(data[k], k, data):
                    res.append(data[k])
        return res
    select = filter

    # def where(self, data, properties):

    # def find_where(self, data, properties):

    def reject(self, data, predicate=None):
        if predicate is None and self.is_func(data):
            return self.partial(self.reject, _, data)
        return self.filter(data, self.negate(predicate))

    def every(self, data, predicate=lambda x, *r: x):
        if predicate is None and self.is_func(data):
            return self.partial(self.every, _, data)
        if type(data) is list or type(data) is tuple:
            for i in range(len(data)):
                if not predicate(data[i], i, data):
                    return False
        elif type(data) is dict:
            for k in data.keys():
                if not predicate(data[k], k, data):
                    return False
        return True

    def some(self, data, predicate=lambda x, *r: x):
        if predicate is None and self.is_func(data):
            return self.partial(self.every, _, data)
        if type(data) is list or type(data) is tuple:
            for i in range(len(data)):
                if predicate(data[i], i, data):
                    return True
        elif type(data) is dict:
            for k in data.keys():
                if predicate(data[k], k, data):
                    return True
        return False
    any = some

    def contains(self, data, item, fromIndex=0):
        data = list(data.values())[fromIndex:] if type(data) is dict else data[fromIndex:]
        return item in data
    includes = contains

    def pluck(self, data, key=None):
        if key is None:
            return self.partial(self.pluck, _, data)

        def iter(d, *r):
            if self.is_list_or_tuple(d) and key >= len(d):
                return None
            if d is dict and key not in d.keys():
                return None
            return d[key]
        return self.map(data, iter)

    def max(self, data, iteratee=lambda x, *r: x):
        if iteratee is None and self.is_func(data):
            return self.partial(self.max, _, data)
        if self.is_list_or_tuple(data):
            res, tmp = (data[0], iteratee(data[0], 0, data))
            for i in range(1, len(data)):
                cmp = iteratee(data[i], i, data)
                if cmp > tmp:
                    tmp, res = (cmp, data[i])
        else:
            keys = list(data.keys())
            res, tmp = (data[keys[0]], iteratee(data[keys[0]], keys.pop(0), data))
            for k in keys:
                cmp = iteratee(data[k], k, data)
                if cmp > tmp:
                    tmp, res = (cmp, data[k])
        return res

    def min(self, data, iteratee=lambda x, *r: x):
        if iteratee is None and self.is_func(data):
            return self.partial(self.min, _, data)
        if self.is_list_or_tuple(data):
            res, tmp = (data[0], iteratee(data[0], 0, data))
            for i in range(1, len(data)):
                cmp = iteratee(data[i], i, data)
                if cmp < tmp:
                    tmp, res = (cmp, data[i])
        else:
            keys = list(data.keys())
            res, tmp = (data[keys[0]], iteratee(data[keys[0]], keys.pop(0), data))
            for k in keys:
                cmp = iteratee(data[k], k, data)
                if cmp < tmp:
                    tmp, res = (cmp, data[k])
        return res

    # def sortBy(self, data, iteratee):

    # def groupBy(self, data, iteratee):

    # def indexBy(self, data, iteratee):

    # def countBy(self, data, iteratee):

    # def shuffle(self, data):

    # def sample(self, data, *n):

    # def to_array(self, data):

    # def size(self, data):

    # def partition(self, data, predicate):

    # Arrays
    def first(self, arr, num=None):
        if num is None:
            return arr[0]
        return arr[0:num]
    head = take = first

    def initial(self, arr, num=1):
        if num is 0:
            return arr[0:]
        else:
            return arr[0:-num]

    def last(self, arr, num=None):
        if num is None:
            return arr[-1]
        return arr[-num:]

    def rest(self, arr, num=1):
        return arr[num:len(arr)]
    tail = drop = rest

    def compact(self, arr):
        return self.filter(arr, lambda x, *r: x)

    def flatten(self, arr, shallow=False):
        res = []

        def flat(value):
            for val in value:
                if not self.is_list_or_tuple(val):
                    res.append(val)
                elif shallow:
                    self.each(val, lambda v, *rest: res.append(v))
                else:
                    flat(val)
        flat(arr)
        return res

    def uniq(self, arr, iteratee=None):
        res, tmp, cmp = ([], [], self.map(arr, iteratee) if iteratee else arr)
        for i in range(len(arr)):
            if cmp[i] not in tmp:
                tmp.append(cmp[i])
                res.append(arr[i])
        return res
    unique = uniq

    def without(self, arr, *values):
        return self.difference(arr, values)

    def intersection(self, arr, *args):
        res, flag = ([], True)
        for item in arr:
            if item in res: continue
            for cmp in args:
                if item not in cmp:
                    flag = False
                    break
            if flag:
                res.append(item)
            else:
                flag = True
        return res

    def union(self, *arrays):
        res = []
        for arr in arrays:
            for v in arr:
                if v not in res:
                    res.append(v)
        return res

    def difference(self, arr, *others):
        res, cmp = ([], self.flatten(others))
        for a in arr:
            if type(a) is dict:
                for c in cmp:
                    if a is not c:
                        res.append(a)
            elif a not in cmp:
                res.append(a)
        return res

    def zip(self, *arrays):
        return self.unzip(arrays)

    def unzip(self, array):
        res, ran = ([], range(len(array and self.max(array, lambda a, *r: len(a)))))
        for i in ran:
            res.append(self.pluck(array, i))
        return res

    def object(self, arr, values=None):
        res = {}
        if values:
            for i, key in enumerate(arr):
                res[key] = values[i]
        else:
            for a in arr:
                res[a[0]] = a[1]
        return res

    def sorted_i(self, data, obj, iteratee=lambda x: x):
        if self.is_func(data):
            return self.partial(self.sorted_i, _, _, data)

        value, low, high = (iteratee(obj), 0, len(data))
        while low < high:
            mid = (low + high) // 2
            if iteratee(data[mid]) < value:
                low = mid + 1
            else:
                high = mid
        return low
    sortedIndex = sorted_index = sorted_i

    def find_i(self, arr, predicate=lambda x, *r: x):
        if self.is_func(arr):
            return self.partial(self.find_i, ___, arr)

        for i, v in enumerate(arr):
            if predicate(v, i, arr):
                return i
        return -1
    findIndex = find_index = find_i

    def find_last_i(self, arr, predicate=lambda x, *r: x):
        if self.is_func(arr):
            return self.partial(self.find_i, ___, arr)

        for i in range(len(arr)-1, -1, -1):
            if predicate(arr[i], i, arr):
                return i
        return -1
    findLastIndex = find_last_index = find_last_i

    def index_of(self, arr, item, idx=0):
        if self.is_list_or_tuple(arr):
            if idx is bool and idx:
                idx = self.sorted_i(arr, item)
                return idx if arr[idx] is item else -1
            for i in range(idx, len(arr)):
                if arr[i] is item:
                    return i
        return -1
    indexOf = index_of

    def last_index_of(self, arr, item, idx=0):
        if self.is_list_or_tuple(arr):
            if idx is bool and idx:
                return self.find_last_i(arr, lambda x, *r: x is item)
            for i in range(len(arr)-1, -1, -1):
                if arr[i] is item:
                    return i
        return -1
    lastIndexOf = last_index_of

    def range(self, start, stop=None, step=None):
        if stop is None:
            return list(range(start))
        if step is None:
            return list(range(start, stop))
        return list(range(start, stop, step))

    # Utility
    identity = idtt = lambda self, val, *rest: val

    always = const = lambda self, val, *rest: lambda *args: val

    # Objects
    def isEqual(self, obj1, obj2=None):
        if obj2 is None:
            return self.partial(self.isEqual, _, obj1)
        return obj1 == obj2

    def isEmpty(self, obj=None):
        if obj is None:
            return True
        elif obj == "":
            return True
        elif len(obj) == 0:
            return True
        return False

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

    def is_bool(self, val):
        return type(val) is bool
    isBool = is_bool

    def is_num(self, val):
        return isinstance(val, (int, float, complex))
    isNumber = is_number = is_num

    def is_mr(self, val):
        return self.is_dict(val) and val.get('_mr')

    def isType(self, obj):
        return type(obj) is type

    def isBoolean(self, obj):
        return type(obj) is bool

    def isInt(self, obj):
        return type(obj) is int

    def isString(self, obj):
        return type(obj) is str

    def mr(self, *args):
        return {'value': args, '_mr': True}

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
        if type(obj) is not dict:
            return None
        for k in obj.keys():
            if predicate(obj[k], k, obj):
                return k
        return None
    findKey = find_key = find_k

    def negate(self, predicate):
        return lambda *args: not predicate(*args)

    def keys(self, obj):
        if type(obj) is not dict:
            return []
        return obj.keys()

    def values(self, obj):
        if type(obj) is not dict:
            return []
        return obj.values()

    def val(self, obj, *keys):
        if len(keys) is 1:
            try:
                neww = obj[keys[0]]
            except:
                neww = []
        else:
            neww = []
            for key in keys:
                try:
                    neww.append(obj[key])
                except:
                    continue
        return neww

    def property(self, key):
        return self.partial(self.val, _, key)

    def propertyOf(self, key):
        return self.partial(self.val, key, _)

    def mapObject(self, obj, iteratee=None):
        if iteratee is None and self.is_func(obj):
            return self.partial(self.mapObject, _, obj)
        res = {}
        for key in obj.keys():
            res[key] = iteratee(float(obj[key]), key, obj)
        return res

    # def pairs(self, obj):
    #     res = []
    #     for val in obj.items():
    #         res.append(list(val))
    #     return res

    def pairs(self, obj):
        res = []
        for key in obj:
            res.append([key, obj[key]])
        return res

    def invert(self, obj):
        res = {}
        for key in obj.keys():
            res[obj[key]] = key
        return res

    def has(self, obj, *keys):
        for key in keys:
            try:
                if obj[key]:
                   res = True
            except:
                return False
        return res

    def extend(self, dest, *sources):
        sources = list(sources)
        for i in sources:
            dest.update(i)
        return dest

    def defaults(self, dest, *sources):
        sources = self.extend({}, *sources)
        for key in sources:
            dest.setdefault(key , sources[key])
        return dest

    def pick(self, obj, *keys):
        if len(keys) is 0:
            return self.partial(self.pick, _, obj)
        res = {}
        if self.is_func(keys[0]):
            for key in obj:
                if keys[0](obj[key], key, obj):
                    res[key] = obj[key]
        else:
            flat = _.flatten(keys)
            for key in flat:
                res[key] = obj[key]
        return res

    def omit(self, obj, *keys):
        if len(keys) is 0:
            return self.partial(self.omit, _, obj)
        res = obj.copy()
        if self.is_func(keys[0]):
            for key in obj:
                if keys[0](obj[key], key, obj):
                    del res[key]
        else:
            flat = _.flatten(keys)
            for key in flat:
                if res[key]:
                    del res[key]
        return res

    def clone(self, obj):
        import copy
        return copy.copy(obj)

    def val2(self, obj, key):
        try:
            return obj[key]
        except:
            return ""

    def matcher(self, obj, *attrs):
        if len(attrs) is 0 :
            return self.partial(self.matcher, _, obj)
        def is_match(obj):
            attr = attrs[0]
            keys = self.keys(attr)
            for key in keys:
                if attr[key] != self.val2(obj, key) or key not in obj:
                    return 0
            return 1
        return is_match(obj)

#     function
    def memoize(self, func, hasher=None):
        if hasher is None:
            hasher = lambda x: x
        cache = {}

        def memoized(key):
            address = hasher(key)
            if address not in cache:
                cache[address] = func(address)
            return cache[address]

        return memoized

    def delay(self, func, wait, *args):

        def call_it():
            if len(args) is 0:
                return func()
            else:
                if self.is_func(args[0]):
                    return func(args[0])
                else:
                    return func(args)

        t = Timer((float(wait)/float(1000)), call_it)
        t.start()

    def defer(self, func, *args):
        # _.defer = _.partial(_.delay, _, 1);
        return self.delay(func, 1, *args)


_ = Partial()
__ = _.pipe
