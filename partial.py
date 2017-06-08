# Partial.py 1.0
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
def __partial(func, *parts):
    parts1, parts2, ___idx = ([], [], len(parts))
    for i in range(___idx):
        if parts[i] == ___:
            ___idx = i
        elif i < ___idx:
            parts1.append(parts[i])
        else:
            parts2.append(parts[i])

    if _.is_asy(func):
        async def asy_partial(*args):
            args1, args2, rest = (parts1[:], parts2[:], list(args))
            for j in range(len(args1)):
                if args1[j] == _:
                    args1[j] = rest.pop(0)
            for j in range(len(args2) - 1, -1, -1):
                if args2[j] == _:
                    args2[j] = rest.pop()
            return await func(*(args1 + rest + args2))
        return asy_partial

    def _partial(*args):
        args1, args2, rest = (parts1[:], parts2[:], list(args))
        for j in range(len(args1)):
            if args1[j] == _:
                args1[j] = rest.pop(0)
        for j in range(len(args2)-1, -1, -1):
            if args2[j] == _:
                args2[j] = rest.pop()
        return func(*(args1 + rest + args2))
    return _partial
_ = __partial
_.partial = __partial


def __go(seed, *funcs):
    seed = seed() if _.is_func(seed) else seed
    for func in funcs:
        if func is __:
            seed = __
        elif _.is_mr(seed):
            seed = func(*seed.get('value'))
        else:
            seed = func() if seed is __ else func(seed)
    return seed
_.go = __go


def __pipe(*funcs):
    for func in funcs:
        if _.is_asy(func):
            async def asy_pipe(*seed):
                return await _.asy.go(seed[0] if len(seed) == 1 else _.mr(*seed), *funcs)
            return asy_pipe

    return lambda *seed: _.go(seed[0] if len(seed) == 1 else _.mr(*seed), *funcs)
_.pipe = __ = __pipe


# Collections
def __each(data, iteratee=None):
    if iteratee is None and _.is_func(data):
        return _(_.asy.each if _.is_asy(data) else _.each, _, data)
    if _.is_asy(iteratee):
        return _.asy.each(data, iteratee)
    if type(data) is list or type(data) is tuple:
        for i in range(len(data)):
            iteratee(data[i], i, data)
    elif type(data) is dict:
        for k in data.keys():
            iteratee(data[k], k, data)
_.each = _.forEach = __each


def __map(data, iteratee=None):
    if iteratee is None and _.is_func(data):
        return _(_.asy.map if _.is_asy(data) else _.map, _, data)
    if _.is_asy(iteratee):
        return _.asy.map(data, iteratee)
    res = []
    if type(data) is list or type(data) is tuple:
        for i in range(len(data)):
            res.append(iteratee(data[i], i, data))
    elif type(data) is dict:
        for k in data.keys():
            res.append(iteratee(data[k], k, data))
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
        for i in range(len(data)):
            if predicate(data[i], i, data):
                return data[i]
    elif type(data) is dict:
        for k in data.keys():
            if predicate(data[k], k, data):
                return data[k]
    return None
_.find = _.detect = __find


def __filter(data, predicate=None):
    if predicate is None and _.is_func(data):
        return _(_.asy.filter if _.is_asy(data) else _.filter, _, data)
    if _.is_asy(predicate):
        return _.asy.filter(data, predicate)
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
        return _(_.asy.reject if _.is_asy(data) else _.filter, _, data)
    if _.is_asy(predicate):
        return _.asy.reject(data, predicate)
    res = []
    if type(data) is list or type(data) is tuple:
        for i in range(len(data)):
            if not predicate(data[i], i, data):
                res.append(data[i])
    elif type(data) is dict:
        for k in data.keys():
            if not predicate(data[k], k, data):
                res.append(data[k])
    return res
_.reject = __reject


def __every(data, predicate=lambda x, *r: x):
    if _.is_func(data):
        return _(_.asy.every if _.is_asy(data) else _.every, _, data)
    if _.is_asy(predicate):
        return _.asy.every(data, predicate)
    if type(data) is list or type(data) is tuple:
        for i in range(len(data)):
            if not predicate(data[i], i, data):
                return False
    elif type(data) is dict:
        for k in data.keys():
            if not predicate(data[k], k, data):
                return False
    return True
_.every = __every


def __some(data, predicate=lambda x, *r: x):
    if _.is_func(data):
        return _(_.asy.some if _.is_asy(data) else _.some, _, data)
    if _.is_asy(predicate):
        return _.asy.some(data, predicate)
    if type(data) is list or type(data) is tuple:
        for i in range(len(data)):
            if predicate(data[i], i, data):
                return True
    elif type(data) is dict:
        for k in data.keys():
            if predicate(data[k], k, data):
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
    iter = iteratee if _.is_func(iteratee) else lambda o: o[iteratee]
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
    iter = iteratee if _.is_func(iteratee) else lambda o: o[iteratee]
    res, arr = ({}, _.map(data, iter))
    for i, v in enumerate(arr):
        res[v] = data[i]
    return res
_.index_by = _.indexBy = __index_by


def __count_by(data, iteratee=lambda x, *r: x):
    if _.is_func(data) or type(data) is str:
        return _(_.count_by, _, data)
    iter = iteratee if _.is_func(iteratee) else lambda o: o[iteratee]
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
def __first(arr, n=None):
    if n is None:
        return arr[0]
    return arr[0:n]
_.first = _.head = _.take = __first


def __initial(arr, n=1):
    if n is 0:
        return arr[0:]
    else:
        return arr[0:-n]
_.initial = __initial


def __last(arr, n=None):
    if n is None:
        return arr[-1]
    return arr[-n:]
_.last = __last


def __rest(arr, n=1):
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
    # print(res, tmp, cmp)
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


def __sorted_i(data, obj, iteratee=lambda x, *r: x):
    if _.is_func(data):
        return _(_.sorted_i, _, _, data)

    value, low, high = (iteratee(obj), 0, len(data))
    while low < high:
        mid = (low + high) // 2
        if iteratee(data[mid]) < value:
            low = mid + 1
        else:
            high = mid
    return low
_.sort_i = _.sortedIndex = _.sorted_index = __sorted_i


def __find_i(arr, predicate=lambda x, *r: x):
    if _.is_func(arr):
        return _(_.find_i, ___, arr)

    for i, v in enumerate(arr):
        if predicate(v, i, arr):
            return i
    return -1
_.find_i = _.findIndex = _.find_index = __find_i


def __find_last_i(arr, predicate=lambda x, *r: x):
    if _.is_func(arr):
        return _(_.find_i, ___, arr)

    for i in range(len(arr)-1, -1, -1):
        if predicate(arr[i], i, arr):
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


# Utility
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


def __is_dictionary(o, *r):
    return type(o) is dict
_.is_dict = _.isDictionary = _.is_dictionary = __is_dictionary


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


def __to_mr(args):
    return {'value': args, '_mr': True}
_.mr_to = __to_mr


def __find_i(arr, predicate=None):
    if predicate is None and _.is_func(arr):
        return _(_.find_i, _, arr)
    if type(arr) is dict:
        return -1
    for i in range(len(arr)):
        if predicate(arr[i], i, arr):
            return i
    return -1
_.find_i = _.findIndex = _.find_index = __find_i


def __find_k(obj, predicate):
    if predicate is None and _.is_func(obj):
        return _(_.find_k, _, obj)
    if type(obj) is not dict:
        return None
    for k in obj.keys():
        if predicate(obj[k], k, obj):
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
        return {key: obj[key] for key in obj if key[0](obj[key], key, obj)}
    else:
        return {key: obj[key] for key in _.flatten(keys)}
_.pick = __pick


def __omit(obj, *keys):
    if len(keys) is 0:
        return _(_.omit, _, obj)
    res = obj.copy()
    if _.is_func(keys[0]):
        for key in obj:
            if keys[0](obj[key], key, obj):
                del res[key]
    else:
        flat = _.flatten(keys)
        for key in flat:
            if res[key]:
                del res[key]
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
def __memoize(func, hasher=None):
    if hasher is None:
        hasher = lambda x: x
    cache = {}

    def memoized(key):
        address = hasher(key)
        if address not in cache:
            cache[address] = func(address)
        return cache[address]

    return memoized
_.memoize = __memoize


def __delay(func, wait, *args):
    def call_it():
        if len(args) is 0:
            return func()
        else:
            if _.is_func(args[0]):
                return func(args[0])
            else:
                return func(*args)

    Timer((float(wait)/float(1000)), call_it).start()
_.delay = __delay


def __defer(func, *args):
    return _.delay(func, 1, *args)
_.defer = __defer


def __retrn(func, *args):
    return func() if len(args) == 0 else func(*args)


def __throttle(func, wait):
    previous = 0
    timeout = False

    def throttled(*args):
        nonlocal previous, timeout
        result = going = None
        now = time.time()
        remaining = wait - (now - previous)

        def later():
            nonlocal timeout, result
            timeout = False
            result = __retrn(func, *args)

        if remaining <= 0:
            if timeout is True:
                going.cancel()
                timeout = False
            previous = now
            result = __retrn(func, *args)
        elif timeout is False:
            timeout = True
            going = Timer(remaining, later)
            going.start()
        return result

    return throttled
_.throttle = __throttle


def __debounce(func, wait):
    wait = float(wait)/float(1000)

    def debounced(*args):
        def call_it():
            return __retrn(func, *args)
        try:
            debounced.t.cancel()
        except:
            pass
        debounced.t = Timer(wait, call_it)
        debounced.t.start()

    return debounced
_.debounce = __debounce


def __after(times, func):
    def aftered(*args):
        nonlocal times
        times -= 1
        if times < 1:
            return __retrn(func, *args)
    return aftered
_.after = __after


def __before(times, func):
    memo = None

    def befored(*args):
        nonlocal times, memo
        times -= 1
        if times < 0:
            return memo
        memo = __retrn(func, *args)
        return memo
    return befored
_.before = __before


def __once(func):
    return _.before(1, func)
_.once = __once


# Utilities
def __is_async(func):
    return asyncio.iscoroutinefunction(func)
_.is_asy = _.is_async = __is_async


def __is_mr(*o):
    return type(o[0]) is dict and o[0].get('_mr')
_.is_mr = __is_mr


def __mr(*args):
    return {'value': args, '_mr': True}
_.mr = __mr


def __tap(*fns):
    fns = __(*fns)

    def tap(*args):
        args = _.to_mr(args) if len(args) > 1 else args[0] if args[0] else __
        return _.go(args, fns, _.const(args))
    return tap
_.tap = __tap

_.hi = _.tap(print)


# Async Series
def __asy(): pass
_.asy = __asy


async def __asy_go(seed, *funcs):
    if _.is_func(seed):
        seed = await seed() if _.is_asy(seed) else seed()
    if asyncio.iscoroutine(seed):
        seed = await seed

    for func in funcs:
        if func is __:
            seed = __
        elif asyncio.iscoroutinefunction(func):
            seed = await func(*seed.get('value')) if _.is_mr(seed) else await func(seed)
        else:
            seed = func(*seed.get('value')) if _.is_mr(seed) else func() if seed is __ else func(seed)
            if asyncio.iscoroutine(seed):
                seed = await seed
    return seed
_.asy.go = __asy_go


def __asy_pipe(*funcs):
    async def asy_pipe(*seed):
        return await _.asy.go(seed[0] if len(seed) == 1 else _.mr(*seed), *funcs)

    return asy_pipe
_.asy.pipe = __asy_pipe


async def __asy_each(data, iteratee=None):
    if iteratee is None and _.is_func(data):
        return _(_.asy.each, _, data)
    if type(data) is list or type(data) is tuple:
        for i in range(len(data)):
            await iteratee(data[i], i, data)
    elif type(data) is dict:
        for k in data.keys():
            await iteratee(data[k], k, data)
_.asy.each = __asy_each


async def __asy_map(data, iteratee=None):
    if iteratee is None and _.is_func(data):
        return _(_.asy.map, _, data)
    res = []
    if type(data) is list or type(data) is tuple:
        for i in range(len(data)):
            res.append(await iteratee(data[i], i, data))
    elif type(data) is dict:
        for k in data.keys():
            res.append(await iteratee(data[k], k, data))
    return res
_.asy.map = __asy_map


async def __asy_reduce(data, iteratee=None, memo=None):
    if _.is_func(data):
        return _(_.asy.reduce, _, data, iteratee)
    if type(data) is list or type(data) is tuple:
        if memo is None:
            memo = data.pop(0)
        for i in range(len(data)):
            memo = await iteratee(memo, data[i], i, data)
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
        for i in range(len(data)):
            if await predicate(data[i], i, data):
                return data[i]
    elif type(data) is dict:
        for k in data.keys():
            if await predicate(data[k], k, data):
                return data[k]
    return None
_.asy.find = __asy_find


async def __asy_filter(data, predicate=None):
    if predicate is None and _.is_func(data):
        return _(_.asy.filter, _, data)
    res = []
    if type(data) is list or type(data) is tuple:
        for i in range(len(data)):
            if await predicate(data[i], i, data):
                res.append(data[i])
    elif type(data) is dict:
        for k in data.keys():
            if await predicate(data[k], k, data):
                res.append(data[k])
    return res
_.asy.filter = __asy_filter


async def __asy_reject(data, predicate=None):
    if predicate is None and _.is_func(data):
        return _(_.asy.reject, _, data)
    res = []
    if type(data) is list or type(data) is tuple:
        for i in range(len(data)):
            if not await predicate(data[i], i, data):
                res.append(data[i])
    elif type(data) is dict:
        for k in data.keys():
            if not await predicate(data[k], k, data):
                res.append(data[k])
    return res
_.asy.reject = __asy_reject


async def __asy_every(data, predicate=lambda x, *r: x):
    if _.is_func(data):
        return _(_.asy.every, _, data)
    if type(data) is list or type(data) is tuple:
        for i in range(len(data)):
            if not await predicate(data[i], i, data):
                return False
    elif type(data) is dict:
        for k in data.keys():
            if not await predicate(data[k], k, data):
                return False
    return True
_.asy.every = __asy_every


async def __asy_some(data, predicate=lambda x, *r: x):
    if _.is_func(data):
        return _(_.some, _, data)
    if type(data) is list or type(data) is tuple:
        for i in range(len(data)):
            if await predicate(data[i], i, data):
                return True
    elif type(data) is dict:
        for k in data.keys():
            if await predicate(data[k], k, data):
                return True
    return False
_.asy.some = __asy_some

___ = {}