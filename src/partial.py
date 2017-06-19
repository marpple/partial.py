# Partial.py 0.1.4
# Project Lead - Indong Yoo
# Maintainers - Jeongik Park, Joeun Ha
# (c) 2017 Marpple. MIT Licensed.
from threading import Timer
import time
import copy
import types
import random
import asyncio


# partial, go, pipe
def __partial(fn, *parts):
    parts1, parts2, ___idx = ([], [], len(parts))
    for i in range(___idx):
        if parts[i] == ___:
            ___idx = i
        elif i < ___idx:
            parts1.append(parts[i])
        else:
            parts2.append(parts[i])

    if _.is_asy(fn):
        async def asy_partial(*args):
            args1, args2, rest = (parts1[:], parts2[:], list(args))
            for j, v in enumerate(args1):
                if v == _:
                    args1[j], rest = _.shift(rest)
            for j, v in reversed(list(enumerate(args2))):
                if v == _:
                    args2[j], rest = _.pop(rest)
            return await fn(*(args1 + rest + args2))
        return asy_partial

    def _partial(*args):
        args1, args2, rest = (parts1[:], parts2[:], list(args))
        for j, v in enumerate(args1):
            if v == _:
                args1[j], rest = _.shift(rest)
        for j, v in reversed(list(enumerate(args2))):
            if v == _:
                args2[j], rest = _.pop(rest)
        return fn(*(args1 + rest + args2))
    return _partial
_ = __partial
_.partial = __partial


def __go(seed, *fns):
    seed = seed() if _.is_func(seed) else seed
    lazys, fl = ([], len(fns))
    for i, fn in enumerate(fns):
        if hasattr(fn, '_p_go_lazy'):
            lazys.append(fn)
            p_i = i + 1
            if fl == p_i or hasattr(fns[p_i], '_p_go_lazy') is False or hasattr(fn, '_p_lze'):
                seed = fn._p_go_lazy(lazys, seed)
        elif fn is __:
            seed = __
        elif _.is_mr(seed):
            seed = fn(*seed['value'])
        else:
            seed = fn() if seed is __ else fn(seed)
    return seed
_.go = __go


def __pipe(*fns):
    for fn in fns:
        if _.is_asy(fn):
            async def asy_pipe(*seed):
                return await _.asy.go(seed[0] if len(seed) == 1 else _.mr(*seed), *fns)
            return asy_pipe

    return lambda *seed: _.go(seed[0] if len(seed) == 1 else _.mr(*seed), *fns)
_.pipe = __ = __pipe


# Collections
def __each(data, iteratee=None):
    if iteratee is None and _.is_func(data):
        return _(_.asy.each if _.is_asy(data) else _.each, _, data)
    if _.is_asy(iteratee):
        return _.asy.each(data, iteratee)
    if type(data) is list or type(data) is tuple:
        for i, v in enumerate(data):
            iteratee(v, i, data)
    elif type(data) is dict:
        for k, v in data.items():
            iteratee(v, k, data)
_.each = _.forEach = __each


def __map(data, iteratee=None):
    if iteratee is None and _.is_func(data):
        return _(_.asy.map if _.is_asy(data) else _.map, _, data)
    if _.is_asy(iteratee):
        return _.asy.map(data, iteratee)
    res = []
    if type(data) is list or type(data) is tuple:
        for i, v in enumerate(data):
            res.append(iteratee(v, i, data))
    elif type(data) is dict:
        for k, v in data.items():
            res.append(iteratee(v, k, data))
    return res
_.map = _.collect = __map


def __reduce(data, iteratee=None, memo=None):
    if _.is_func(data):
        return _(_.asy.reduce if _.is_asy(data) else _.reduce, _, data, iteratee)
    if _.is_asy(iteratee):
        return _.asy.reduce(data, iteratee, memo)
    if type(data) is list or type(data) is tuple:
        if memo is None:
            memo = data.pop(0)
        for i, v in enumerate(data):
            memo = iteratee(memo, v, i, data)
    elif type(data) is dict:
        keys = data.keys()
        if memo is None:
            keys = list(keys)
            memo = data[keys.pop(0)]
        for k in keys:
            memo = iteratee(memo, data[k], k, data)
    return memo
_.reduce = _.inject = _.fold = __reduce


def __reduce_right(data, iteratee=None, memo=None):
    if _.is_func(data):
        return _(_.asy.reduce_right if _.is_asy(data) else _.reduce_right, _, data, iteratee)
    if _.is_asy(iteratee):
        return _.asy.reduce_right(data, iteratee, memo)
    if type(data) is list or type(data) is tuple:
        if memo is None:
            memo = data.pop()
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
_.reduce_right = _.foldr = _.reduceRight = __reduce_right


def __find(data, predicate=None):
    if predicate is None and _.is_func(data):
        return _(_.asy.find if _.is_asy(data) else _.find, _, data)
    if _.is_asy(predicate):
        return _.asy.find(data, predicate)
    if type(data) is list or type(data) is tuple:
        for i, v in enumerate(data):
            if predicate(v, i, data):
                return v
    elif type(data) is dict:
        for k, v in data.items():
            if predicate(v, k, data):
                return v
    return None
_.find = _.detect = __find


def __filter(data, predicate=None):
    if predicate is None and _.is_func(data):
        return _(_.asy.filter if _.is_asy(data) else _.filter, _, data)
    if _.is_asy(predicate):
        return _.asy.filter(data, predicate)
    res = []
    if type(data) is list or type(data) is tuple:
        for i, v in enumerate(data):
            if predicate(v, i, data):
                res.append(v)
    elif type(data) is dict:
        for k, v in data.items():
            if predicate(v, k, data):
                res.append(v)
    return res
_.filter = _.select = __filter


def __where(data, attrs=None):
    if attrs is None:
        return _.filter(lambda o, *r: _.is_match(o, attrs))
    return _.filter(data, lambda o, *r: _.is_match(o, attrs))
_.where = __where


def __find_where(data, attrs):
    if attrs is None:
        return _.find(lambda o, *r: _.is_match(o, attrs))
    return _.find(data, lambda o, *r: _.is_match(o, attrs))
_.findWhere = _.findWhere = __find_where


def __reject(data, predicate=None):
    if predicate is None and _.is_func(data):
        return _(_.asy.reject if _.is_asy(data) else _.reject, _, data)
    if _.is_asy(predicate):
        return _.asy.reject(data, predicate)
    res = []
    if type(data) is list or type(data) is tuple:
        for i, v in enumerate(data):
            if not predicate(v, i, data):
                res.append(v)
    elif type(data) is dict:
        for k, v in data.items():
            if not predicate(v, k, data):
                res.append(v)
    return res
_.reject = __reject


def __every(data, predicate=lambda x, *r: x):
    if _.is_func(data):
        return _(_.asy.every if _.is_asy(data) else _.every, _, data)
    if _.is_asy(predicate):
        return _.asy.every(data, predicate)
    if type(data) is list or type(data) is tuple:
        for i, v in enumerate(data):
            if not predicate(v, i, data):
                return False
    elif type(data) is dict:
        for k, v in data.items():
            if not predicate(v, k, data):
                return False
    return True
_.every = __every


def __some(data, predicate=lambda x, *r: x):
    if _.is_func(data):
        return _(_.asy.some if _.is_asy(data) else _.some, _, data)
    if _.is_asy(predicate):
        return _.asy.some(data, predicate)
    if type(data) is list or type(data) is tuple:
        for i, v in enumerate(data):
            if predicate(v, i, data):
                return True
    elif type(data) is dict:
        for k, v in data.items():
            if predicate(v, k, data):
                return True
    return False
_.some = _.any = __some


def __contains(data, item, idx=0):
    data = list(data.values())[idx:] if type(data) is dict else data[idx:]
    return item in data
_.contains = _.includes = __contains


def __invoke(data, method, *args):
    is_func = _.is_func(method)

    def iter(value, *r):
        if is_func:
            return method(value, *args)
        else:
            return getattr(value, method)(*args)
    return _.map(data, iter)
_.invoke = __invoke


def __pluck(data, key=None):
    if key is None:
        return _(_.pluck, _, data)

    def iter(d, *r):
        if _.is_list_or_tuple(d) and key >= len(d):
            return None
        if d is dict and key not in d.keys():
            return None
        return d[key]
    return _.map(data, iter)
_.pluck = __pluck


def __max(data, iteratee=lambda x, *r: x):
    if _.is_func(data):
        return _(_.max, _, data)
    if _.is_list_or_tuple(data):
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
_.max = __max


def __min(data, iteratee=lambda x, *r: x):
    if _.is_func(data):
        return _(_.min, _, data)
    if _.is_list_or_tuple(data):
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
_.min = __min


def __sort_by(data, iteratee=lambda x, *r: x):
    if _.is_func(data) or type(data) is str:
        return _(_.sort_by, _, data)
    res, iter = (list(data), iteratee if _.is_func(iteratee) else lambda o, *r: o[iteratee])
    res.sort(key=iter)
    return res
_.sort_by = _.sortBy = __sort_by


def __group_by(data, iteratee=lambda x, *r: x):
    if _.is_func(data) or type(data) is str:
        return _(_.group_by, _, data)
    iter = iteratee if _.is_func(iteratee) else lambda o, *r: o[iteratee]
    res, arr = ({}, _.map(data, iter))
    for i, v in enumerate(arr):
        if _.has(res, v):
            res[v].append(data[i])
        else:
            res[v] = [data[i]]
    return res
_.group_by = _.groupBy = __group_by


def __index_by(data, iteratee=lambda x, *r: x):
    if _.is_func(data) or type(data) is str:
        return _(_.index_by, _, data)
    iter = iteratee if _.is_func(iteratee) else lambda o, *r: o[iteratee]
    res, arr = ({}, _.map(data, iter))
    for i, v in enumerate(arr):
        res[v] = data[i]
    return res
_.index_by = _.indexBy = __index_by


def __count_by(data, iteratee=lambda x, *r: x):
    if _.is_func(data) or type(data) is str:
        return _(_.count_by, _, data)
    iter = iteratee if _.is_func(iteratee) else lambda o, *r: o[iteratee]
    res, arr = ({}, _.map(data, iter))
    for i, v in enumerate(arr):
        try:
            res[v] += 1
        except:
            res[v] = 1
    return res
_.count_by = _.countBy = __count_by


def __shuffle(data):
    cloned = _.values(data) if _.is_dict(data) else data[:]
    random.shuffle(cloned)
    return cloned
_.shuffle = __shuffle


def __sample(data, n=None):
    if n is None:
        return _.shuffle(data)[0]
    return _.shuffle(data)[0:n]
_.sample = __sample


def __to_array(data):
    return list(data.values()) if _.is_dict(data) else list(data)
_.to_array = _.toArray = __to_array


def __size(data):
    if data is None:
        return 0
    return len(data) if _.is_list_or_tuple(data) else len(data.keys())
_.size = __size


def __partition(data, predicate=lambda x, *r: x):
    if _.is_func(data):
        return _(_.partition, _, data)
    if _.is_str(predicate):
        key = predicate
        predicate = lambda x, *r: x[key]
    filtered, rejected = ([], [])
    _.each(data, lambda v, i, d: filtered.append(v) if predicate(v, i, data) else rejected.append(v))
    return [filtered, rejected]
_.partition = __partition


# Arrays
def __first(arr, n=None, guard=None):
    if _.is_num(arr):
        return _(_.first, _, arr)
    if n is None or guard:
        return arr[0]
    return arr[0:n]
_.first = _.head = _.take = __first


def __initial(arr, n=None, guard=None):
    if _.is_num(arr):
        return _(_.initial, _, arr)
    if guard or n is None:
        return arr[0:-1]
    elif n is 0:
        return arr[0:]
    else:
        return arr[0:-n]
_.initial = __initial


def __last(arr, n=None, guard=None):
    if _.is_num(arr):
        return _(_.last, _, arr)
    if n is None or guard:
        return arr[-1]
    return arr[-n:]
_.last = __last


def __rest(arr, n=1, guard=None):
    if _.is_num(arr):
        return _(_.rest, _, arr)
    if guard: n = 1
    return arr[n:len(arr)]
_.rest = _.tail = _.drop = __rest


def __compact(arr):
    return _.filter(arr, lambda x, *r: x)
_.compact = __compact


def __flatten(arr, no_deep=False):
    res = []

    def flat(value):
        for val in value:
            if not _.is_list_or_tuple(val):
                res.append(val)
            elif no_deep:
                _.each(val, lambda v, *rest: res.append(v))
            else:
                flat(val)
    flat(arr)
    return res
_.flatten = __flatten


def __uniq(arr, iteratee=None):
    res, tmp, cmp = ([], [], _.map(arr, iteratee) if iteratee else arr)
    for i, v in enumerate(arr):
        if cmp[i] not in tmp:
            tmp.append(cmp[i])
            res.append(v)
    return res
_.uniq = _.unique = __uniq


def __without(arr, *values):
    return _.difference(arr, values)
_.without = __without


def __intersection(arr, *args):
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
_.intersection = __intersection


def __union(*arrays):
    res = []
    for arr in arrays:
        for v in arr:
            if v not in res:
                res.append(v)
    return res
_.union = __union


def __difference(arr, *others):
    res, cmp = ([], _.flatten(others))
    for a in arr:
        if type(a) is dict:
            for c in cmp:
                if a is not c:
                    res.append(a)
        elif a not in cmp:
            res.append(a)
    return res
_.difference = __difference


def __zip(*arrays):
    return _.unzip(arrays)
_.zip = __zip


def __unzip(array):
    res, ran = ([], range(len(array and _.max(array, lambda a, *r: len(a)))))
    for i in ran:
        res.append(_.pluck(array, i))
    return res
_.unzip = __unzip


def __object(arr, vals=None):
    res = {}
    if vals:
        for i, key in enumerate(arr):
            res[key] = vals[i]
    else:
        for a in arr:
            res[a[0]] = a[1]
    return res
_.object = __object


def __sorted_i(data, obj=None, iteratee=lambda x, *r: x):
    if obj is None:
        return _(_.sorted_i, _, _, data)
    iter = (lambda o, *r: o[iteratee]) if _.is_str(iteratee) else iteratee
    value, low, high = (iter(obj), 0, len(data))
    while low < high:
        mid = (low + high) // 2
        if iter(data[mid]) < value:
            low = mid + 1
        else:
            high = mid
    return low
_.sorted_i = _.sortedIndex = _.sorted_index = __sorted_i


def __find_i(arr, predicate=None):
    if not _.is_list(arr) and predicate is None:
        return _(_.find_i, ___, arr)

    if predicate is None:
        predi = _.idtt
    elif _.is_dict(predicate):
        predi = _.const(predicate)

    for i, v in enumerate(arr):
        if predi(v, i, arr):
            return i
    return -1
_.find_i = _.findIndex = _.find_index = __find_i


def __find_last_i(arr, predicate=None):
    if not _.is_list(arr) and predicate is None:
        return _(_.find_last_i, ___, arr)

    if predicate is None:
        predi = _.idtt
    elif _.is_dict(predicate):
        predi = _.const(predicate)

    for i in range(len(arr)-1, -1, -1):
        if predi(arr[i], i, arr):
            return i
    return -1
_.find_last_i = _.findLastIndex = _.find_last_index = __find_last_i


def __index_of(arr, item, idx=0):
    if _.is_list_or_tuple(arr):
        if idx is bool and idx:
            idx = _.sorted_i(arr, item)
            return idx if arr[idx] is item else -1
        for i in range(idx, len(arr)):
            if arr[i] is item:
                return i
    return -1
_.index_of = _.indexOf = __index_of


def __last_index_of(arr, item, idx=0):
    if _.is_list_or_tuple(arr):
        if idx is bool and idx:
            return _.find_last_i(arr, lambda x, *r: x is item)
        for i in range(len(arr)-1, -1, -1):
            if arr[i] is item:
                return i
    return -1
_.last_index_of = _.lastIndexOf = __last_index_of


def __range(start, stop=None, step=None):
    if stop is None:
        return list(range(start))
    if step is None:
        return list(range(start, stop))
    return list(range(start, stop, step))
_.range = __range


def __pop(arr):
    res = arr[:]
    try:
        return (res.pop(), res)
    except:
        return (None, res)
_.pop = __pop


def __shift(arr):
    res = arr[:]
    try:
        return (res.pop(0), res)
    except:
        return (None, res)
_.shift = __shift


# Objects
def __is_equal(obj1, obj2=None):
    if obj2 is None:
        return _(_.isEqual, _, obj1)
    return obj1 == obj2
_.is_equal = _.isEqual = __is_equal


def __is_empty(obj=None):
    if obj is None:
        return True
    elif obj == "":
        return True
    elif len(obj) == 0:
        return True
    return False
_.is_empty = _.isEmpty = __is_empty


def __is_function(o, *r):
    return isinstance(o, types.FunctionType) or callable(o)
_.is_func = _.isFunction = _.is_function = __is_function


def __is_dict(o, *r):
    return type(o) is dict
_.is_dict = _.isDict = __is_dict


def __is_list(o, *r):
    return type(o) is list
_.is_list = _.isList = __is_list


def __is_tuple(o, *r):
    return type(o) is tuple
_.is_tuple = _.isTuple = __is_tuple


def __is_none(o, *r):
    return o is None
_.is_none = _.isNone = __is_none


def __is_bool(o, *r):
    return type(o) is bool
_.is_bool = _.isBool = __is_bool


def __is_number(o, *r):
    return isinstance(o, (int, float, complex))
_.is_num = _.is_number = _.isNumber = __is_number


def __is_string(o, *r):
    return type(o) is str
_.is_str = _.is_string = _.isString = __is_string


def __is_type(o, *r):
    return type(o) is type
_.is_type = _.isType = __is_type


def __is_list_or_tuple(o):
    t = type(o)
    return t is list or t is tuple
_.is_list_or_tuple = __is_list_or_tuple


def __find_i(arr, predicate=None):
    if predicate is None and _.is_func(arr):
        return _(_.find_i, _, arr)
    if type(arr) is dict:
        return -1
    for i, v in enumerate(arr):
        if predicate(v, i, arr):
            return i
    return -1
_.find_i = _.findIndex = _.find_index = __find_i


def __find_k(obj, predicate):
    if predicate is None and _.is_func(obj):
        return _(_.find_k, _, obj)
    if type(obj) is not dict:
        return None
    for k, v in obj.items():
        if predicate(v, k, obj):
            return k
    return None
_.find_k = _.findKey = _.find_key = __find_k


def __negate(predicate):
    return lambda *args: not predicate(*args)
_.negate = __negate


def __keys(obj):
    return list(obj.keys()) if _.is_dict(obj) else []
_.keys = __keys


def __values(obj):
    return list(obj.values()) if _.is_dict(obj) else []
_.values = __values


def __val(obj, *keys):
    l = len(keys)
    if l is 0:
        return _.property(obj)
    elif l is 1:
        try:
            res = obj[keys[0]]
        except:
            res = None
    else:
        res = []
        for key in keys:
            try:
                res.append(obj[key])
            except:
                continue
    return res
_.val = _.v = __val


def __property(key):
    return _(_.val, _, key)
_.property = __property


def __property_of(key):
    return _(_.val, key, _)
_.property_of = _.propertyOf = __property_of


def __map_object(obj, iteratee=None):
    if iteratee is None and _.is_func(obj):
        return _(_.mapObject, _, obj)
    return {key: iteratee(_.num(obj[key]) if _.is_num(obj[key]) else obj[key], key, obj) for key in obj.keys()}
_.map_object = _.mapObject = __map_object


def __num(str):
    try:
        return int(str)
    except ValueError:
        return float(str)
_.num = __num


def __pairs(obj):
    return [[key, obj[key]] for key in obj]
_.pairs = __pairs


def __invert(obj):
    return {obj[key]: key for key in obj.keys()}
_.invert = __invert


def __functions(obj):
    return sorted([k for i, k in enumerate(obj) if callable(obj[k])])
_.functions = __functions


def __has(obj, *keys):
    for key in keys:
        try:
            if obj[key]:
                res = True
        except:
            return False
    return res
_.has = __has


def __extend(dest, *sources):
    if len(sources) is 0:
        return _(_.pick, _, dest)

    for i in list(sources):
        dest.update(i)
    return dest
_.extend = __extend


def __defaults(dest, *sources):
    if len(sources) is 0:
        return _(_.pick, _, dest)

    sources = _.extend({}, *sources)
    for key in sources:
        dest.setdefault(key, sources[key])
    return dest
_.defaults = __defaults


def __pick(obj, *keys):
    if len(keys) is 0:
        return _(_.pick, _, obj)
    if _.is_func(keys[0]):
        return {k: obj[k] for k in obj if keys[0](obj[k], k, obj)}
    else:
        return {k: obj[k] for k in _.flatten(keys)}
_.pick = __pick


def __omit(obj, *keys):
    if len(keys) is 0:
        return _(_.omit, _, obj)
    res = obj.copy()
    if _.is_func(keys[0]):
        for k in obj:
            if keys[0](obj[k], k, obj):
                del res[k]
    else:
        flat = _.flatten(keys)
        for k in flat:
            if res[k]:
                del res[k]
    return res
_.omit = __omit


def __clone(obj):
    return copy.copy(obj)
_.clone = __clone


def __matcher(attrs):
    return _(_.is_match, _, attrs)
_.matcher = __matcher


def __is_match(obj, attrs, *r):
    for key in attrs.keys():
        if attrs[key] != _.val(obj, key):
            return False
    return True
_.is_match = _.isMatch = __is_match


# Functions
def __memoize(fn, hasher=None):
    if hasher is None:
        hasher = lambda x: x
    cache = {}

    def memoized(key):
        address = hasher(key)
        if address not in cache:
            cache[address] = fn(address)
        return cache[address]

    return memoized
_.memoize = __memoize


def __delay(fn, wait, *args):
    def call_it():
        if len(args) is 0:
            return fn()
        else:
            if _.is_func(args[0]):
                return fn(args[0])
            else:
                return fn(*args)

    Timer((float(wait)/float(1000)), call_it).start()
_.delay = __delay


def __defer(fn, *args):
    return _.delay(fn, 1, *args)
_.defer = __defer


def __retrn(fn, *args):
    return fn() if len(args) == 0 else fn(*args)


def __throttle(fn, wait):
    previous = 0
    timeout = False
    result = going = None
    argss = None

    def later():
        nonlocal timeout, result, previous
        timeout = False
        previous = time.time()
        result = __retrn(fn, *argss)

    def throttled(*args):
        nonlocal previous, timeout, result, going, argss
        argss = args
        now = time.time()
        remaining = wait - (now - previous)
        if remaining <= 0:
            if timeout is True:
                going.cancel()
                timeout = False
            previous = now
            result = __retrn(fn, *args)
        elif timeout is False:
            timeout = True
            going = Timer(remaining, later)
            going.start()
        return result

    return throttled
_.throttle = __throttle


def __debounce(fn, wait):
    wait = float(wait)/float(1000)

    def debounced(*args):
        def call_it():
            return __retrn(fn, *args)
        try:
            debounced.t.cancel()
        except:
            pass
        debounced.t = Timer(wait, call_it)
        debounced.t.start()

    return debounced
_.debounce = __debounce


def __after(times, fn):
    def aftered(*args):
        nonlocal times
        times -= 1
        if times < 1:
            return __retrn(fn, *args)
    return aftered
_.after = __after


def __before(times, fn):
    memo = None

    def befored(*args):
        nonlocal times, memo
        times -= 1
        if times < 1:
            return memo
        memo = __retrn(fn, *args)
        return memo
    return befored
_.before = __before


def __once(fn):
    return _.before(2, fn)
_.once = __once


# Utilities
def _1(*args):
    if _.is_func(args[0]):
        return lambda *a: args[0](a[0])
    return args[0]
_.args0 = _1


def _2(*args):
    if _.is_func(args[0]):
        return lambda *a: args[0](a[0], a[1])
    return args[1]
_.args1 = _2


def _3(*args):
    if _.is_func(args[0]):
        return lambda *a: args[0](a[0], a[1], a[3])
    return args[2]
_.args2 = _3


def __identity(v, *r):
    return v
_.identity = _.idtt = __identity


def __always(v, *r):
    return lambda *args: v
_.always = _.const = __always


def __random(min_num, max_num=None):
    if max_num is None:
        max_num = min_num
        min_num = 0
    return random.randrange(min_num, max_num)


_.bool = lambda v, *r: bool(v)


def __is_async(fn):
    return asyncio.iscoroutinefunction(fn)
_.is_asy = _.is_async = __is_async


def __is_mr(o, *r):
    return type(o) is dict and o.get('_mr')
_.is_mr = __is_mr


def __mr(*args):
    return {'value': args, '_mr': True}
_.mr = __mr


def __to_mr(arg):
    return {'value': arg, '_mr': True}
_.to_mr = __to_mr


def __tap(*fns):
    fns = __(*fns)

    def tap(*args):
        args = _.to_mr(args) if len(args) > 1 else args[0] if args[0] else __
        return _.go(args, fns, _.const(args))
    return tap
_.tap = __tap


_.hi = _.tap(print)


def __all(*args):
    fns = _.last(args)
    if _.is_list(fns):
        return _.all2(*[_.to_mr(_.initial(args))] + fns)
    fns = list(args)
    return lambda *argv: _.all2(*[_.to_mr(argv)] + fns)
_.all = _.share = __all


def __all2(arg, *fns):
    res = []
    for fn in fns:
        tmp = fn(*arg['value']) if _.is_mr(arg) else fn(arg)
        if _.is_mr(tmp):
            for v in tmp:
                res.append(v)
        else:
            res.append(tmp)
    return _.to_mr(res)
_.all2 = __all2


def __spread(*fns):
    def spread(*args):
        return _.mr(*[fns[i](v) for i, v in enumerate(args)])
    return spread
_.spread = __spread


# Async Series
def __asy(): pass
_.asy = __asy


async def __asy_go(seed, *fns):
    if _.is_func(seed):
        seed = await seed() if _.is_asy(seed) else seed()
    if asyncio.iscoroutine(seed):
        seed = await seed

    for fn in fns:
        if fn is __:
            seed = __
        elif asyncio.iscoroutinefunction(fn):
            seed = await fn(*seed['value']) if _.is_mr(seed) else await fn(seed)
        else:
            seed = fn(*seed['value']) if _.is_mr(seed) else fn() if seed is __ else fn(seed)
            if asyncio.iscoroutine(seed):
                seed = await seed
    return seed
_.asy.go = __asy_go


def __asy_pipe(*fns):
    async def asy_pipe(*seed):
        return await _.asy.go(seed[0] if len(seed) == 1 else _.mr(*seed), *fns)

    return asy_pipe
_.asy.pipe = __asy_pipe


async def __asy_each(data, iteratee=None):
    if iteratee is None and _.is_func(data):
        return _(_.asy.each, _, data)
    if type(data) is list or type(data) is tuple:
        for i, v in enumerate(data):
            await iteratee(v, i, data)
    elif type(data) is dict:
        for k, v in data.items():
            await iteratee(v, k, data)
_.asy.each = __asy_each


async def __asy_map(data, iteratee=None):
    if iteratee is None and _.is_func(data):
        return _(_.asy.map, _, data)
    res = []
    if type(data) is list or type(data) is tuple:
        for i, v in enumerate(data):
            res.append(await iteratee(v, i, data))
    elif type(data) is dict:
        for k, v in data.items():
            res.append(await iteratee(v, k, data))
    return res
_.asy.map = __asy_map


async def __asy_reduce(data, iteratee=None, memo=None):
    if _.is_func(data):
        return _(_.asy.reduce, _, data, iteratee)
    if type(data) is list or type(data) is tuple:
        if memo is None:
            memo = data.pop(0)
        for i, v in enumerate(data):
            memo = await iteratee(memo, v, i, data)
    elif type(data) is dict:
        keys = data.keys()
        if memo is None:
            keys = list(keys)
            memo = data[keys.pop(0)]
        for k in keys:
            memo = await iteratee(memo, data[k], k, data)
    return memo
_.asy.reduce = __asy_reduce


async def __asy_reduce_right(data, iteratee=None, memo=None):
    if _.is_func(data):
        return _(_.asy.reduce_right, _, data, iteratee)
    if type(data) is list or type(data) is tuple:
        if memo is None:
            memo = data.pop()
        for i in range(len(data)-1, -1, -1):
            memo = await iteratee(memo, data[i], i, data)
    elif type(data) is dict:
        keys = list(data.keys())
        keys.reverse()
        if memo is None:
            memo = data[keys.pop(0)]
        for k in keys:
            memo = await iteratee(memo, data[k], k, data)
    return memo
_.asy.reduce_right = __asy_reduce_right


async def __asy_find(data, predicate=None):
    if predicate is None and _.is_func(data):
        return _(_.asy.find, _, data)
    if type(data) is list or type(data) is tuple:
        for i, v in enumerate(data):
            if await predicate(v, i, data):
                return data[i]
    elif type(data) is dict:
        for k, v in data.items():
            if await predicate(v, k, data):
                return data[k]
    return None
_.asy.find = __asy_find


async def __asy_filter(data, predicate=None):
    if predicate is None and _.is_func(data):
        return _(_.asy.filter, _, data)
    res = []
    if type(data) is list or type(data) is tuple:
        for i, v in enumerate(data):
            if await predicate(v, i, data):
                res.append(v)
    elif type(data) is dict:
        for k, v in data.items():
            if await predicate(v, k, data):
                res.append(v)
    return res
_.asy.filter = __asy_filter


async def __asy_reject(data, predicate=None):
    if predicate is None and _.is_func(data):
        return _(_.asy.reject, _, data)
    res = []
    if type(data) is list or type(data) is tuple:
        for i, v in enumerate(data):
            if not await predicate(v, i, data):
                res.append(v)
    elif type(data) is dict:
        for k, v in data.items():
            if not await predicate(v, k, data):
                res.append(v)
    return res
_.asy.reject = __asy_reject


async def __asy_every(data, predicate=lambda x, *r: x):
    if _.is_func(data):
        return _(_.asy.every, _, data)
    if type(data) is list or type(data) is tuple:
        for i, v in enumerate(data):
            if not await predicate(v, i, data):
                return False
    elif type(data) is dict:
        for k, v in data.items():
            if not await predicate(v, k, data):
                return False
    return True
_.asy.every = __asy_every


async def __asy_some(data, predicate=lambda x, *r: x):
    if _.is_func(data):
        return _(_.some, _, data)
    if type(data) is list or type(data) is tuple:
        for i, v in enumerate(data):
            if await predicate(v, i, data):
                return True
    elif type(data) is dict:
        for k, v in data.items():
            if await predicate(v, k, data):
                return True
    return False
_.asy.some = __asy_some


# Lazy Series
def L(): pass


def go_lazy(lazys, data):
    res = []
    if hasattr(lazys[0], '_p_lzst'):
        if lazys[0](data):
            return go_strict(lazys, data)
        lazys = lazys[1:]
    for i, v in enumerate(data):
        memo, breaked = (v, False)
        for fn in lazys:
            evaled = fn(memo)
            if hasattr(fn, '_p_lzt_m'):
                memo = evaled
            elif evaled is False:
                breaked = True
                break
        if breaked:
            continue
        res.append(memo)
    return res


def go_lazy_t(lazys, data):
    res, limit = ([], lazys[-1].limit)
    if hasattr(lazys[0], '_p_lzst'):
        if lazys[0](data):
            return go_strict(lazys, data)
        lazys = lazys[1:-1]
    else:
        lazys = lazys[:-1]
    for i, v in enumerate(data):
        memo, breaked = (v, False)
        for fn in lazys:
            evaled = fn(memo)
            if hasattr(fn, '_p_lzt_m'):
                memo = evaled
            elif evaled is False:
                breaked = True
                break
        if breaked:
            continue
        res.append(memo)
        if len(res) == limit:
            break
    return res


def go_lazy_fi(lazys, data):
    ender = lazys[-1]
    if hasattr(lazys[0], '_p_lzst'):
        if lazys[0](data):
            return go_strict(lazys, data)
        lazys = lazys[1:]
    for i, v in enumerate(data):
        memo, breaked = (v, False)
        for fn in lazys:
            evaled = fn(memo)
            if hasattr(fn, '_p_lzt_m'):
                memo = evaled
            elif evaled is False:
                breaked = True
                break
        if breaked:
            continue
        if ender(memo):
            return memo


def go_lazy_s(lazys, data):
    ender = lazys.pop()
    if hasattr(lazys[0], '_p_lzst'):
        if lazys[0](data):
            return go_strict(lazys, data)
        lazys = lazys[1:]
    for i, v in enumerate(data):
        memo, breaked = (v, False)
        for fn in lazys:
            evaled = fn(memo)
            if hasattr(fn, '_p_lzt_m'):
                memo = evaled
            elif evaled is False:
                breaked = True
                break
        if breaked:
            continue
        if ender(memo):
            return True
    return False


def go_lazy_e(lazys, data):
    ender = lazys.pop()
    if hasattr(lazys[0], '_p_lzst'):
        if lazys[0](data):
            return go_strict(lazys, data)
        lazys = lazys[1:]
    for i, v in enumerate(data):
        memo, breaked = (v, False)
        for fn in lazys:
            evaled = fn(memo)
            if hasattr(fn, '_p_lzt_m'):
                memo = evaled
            elif evaled is False:
                breaked = True
                break
        if breaked:
            continue
        if ender(memo) is False:
            return False
    return True


def go_strict(lazys, data):
    def _strict_li(l, *r):
        if hasattr(l, '_p_lzt_m'):
            return _.map(l)
        if hasattr(l, '_p_lzt_ft'):
            return _.filter(l)
        if hasattr(l, '_p_lzt_t'):
            return _.take(l.limit)
        if hasattr(l, '_p_lzt_fi'):
            return _.find(l)
        if hasattr(l, '_p_lzt_s'):
            return _.some(l)
        if hasattr(l, '_p_lzt_e'):
            return _.every(l)

    return _.go(data, *_.map(_.rest(lazys), _strict_li))


def __Lmap(iter):
    iter._p_lzne = iter._p_lzt_m = True
    iter._p_go_lazy = go_lazy
    return iter
L.map = __Lmap


def __Lfilter(iter):
    iter._p_lzne = iter._p_lzt_ft = True
    iter._p_go_lazy = go_lazy
    return iter
L.filter = __Lfilter


def __Lreject(_iter):
    iter = _.negate(_iter)
    iter._p_lzne = True
    iter._p_go_lazy = go_lazy
    return iter
L.reject = __Lreject


def __Lfind(iter):
    iter._p_lze = iter._p_lzt_fi = True
    iter._p_go_lazy = go_lazy_fi
    return iter
L.find = __Lfind


def __Lsome(iter):
    iter._p_lze = iter._p_lzt_s = True
    iter._p_go_lazy = go_lazy_s
    return iter
L.some = __Lsome


def __Levery(iter):
    iter._p_lze = iter._p_lzt_e = True
    iter._p_go_lazy = go_lazy_e
    return iter
L.every = __Levery


def __Ltake(limit):
    def a(): pass
    a._p_go_lazy = go_lazy_t
    a._p_lze = a._p_lzt_t = True
    a.limit = limit
    return a
L.take = __Ltake


def __Lstrict(limit):
    if _.is_num(limit):
        return L.strict(lambda d: len(d) < limit)
    limit._p_lzne = limit._p_lzst = True
    limit._p_go_lazy = True
    return limit
L.strict = __Lstrict
___ = {}
