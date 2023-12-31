import functools
from copy import copy


_set = set

_exception = object()


def get(data, information_path, default=_exception):
    if not isinstance(information_path, list) and not isinstance(
        information_path, tuple
    ):
        information_path = (information_path,)

    try:
        obj = data
        for i in information_path:
            obj = obj[i]
        return obj
    except (KeyError, IndexError):
        if default is _exception:
            raise
        return default


@functools.singledispatch
def set(data, information_path, new_val):
    if not isinstance(information_path, list) and not isinstance(
        information_path, tuple
    ):
        information_path = (information_path,)

    if not information_path:
        return new_val
    data = copy(data)
    i = information_path[0]
    ip = information_path[1:]
    try:
        data[i] = set(data[i], ip, new_val)
    except KeyError:
        if ip:
            raise
        data[i] = new_val
    except IndexError:
        if ip:
            raise
        data.extend([None] * (i - len(data)))
        data.append(new_val)
    return data


@set.register
def _(data: tuple, information_path, new_val):
    cls = type(data)
    i = information_path[0]
    ip = information_path[1:]
    return cls(set(x, ip, new_val) if k == i else x for k, x in enumerate(data))


@functools.singledispatch
def keys(data):
    return range(len(data))


@keys.register
def _(data: dict):
    return data.keys()


@functools.singledispatch
def map(data, f):
    cls = type(data)
    return cls(f(x) for x in data)


@map.register
def _(data: dict, f):
    cls = type(data)
    return cls((k, f(v)) for k, v in data.items())


@functools.singledispatch
def filter(data, f):
    cls = type(data)
    return cls(x for x in data if f(x))


@filter.register
def _(data: dict, f):
    cls = type(data)
    return cls((k, v) for k, v in data.items() if f(v))


def has(data, key) -> bool:
    return key in data


def sum(data, init=0):
    return reduce(data, init, lambda acc, x: acc + x)


@functools.singledispatch
def reduce(data, init, f):
    red = init
    for x in data:
        red = f(red, x)
    return red


@reduce.register
def _(data: dict, init, f):
    return reduce(data.values(), init, f)


def union(a, b):
    seen = _set()
    for c in (a, b):
        for x in c:
            if x not in seen:
                seen.add(x)
                yield x


def intersection(a, b):
    seen = _set(b)
    for x in a:
        if x in seen:
            yield x


@functools.singledispatch
def is_object(obj):
    return False


@is_object.register
def _(obj: list):
    return True


@is_object.register
def _(obj: dict):
    return True


@is_object.register
def _(obj: tuple):
    return True


@functools.singledispatch
def is_empty(obj):
    return False


@is_empty.register
def _(obj: list):
    return not obj


@is_empty.register
def _(obj: dict):
    return not obj


@is_empty.register
def _(obj: tuple):
    return not obj


@functools.singledispatch
def merge(data1, data2):
    if data2 is None:
        return data1
    else:
        return data2


@merge.register
def _(data1: dict, data2: dict):
    out = {}
    for k in union(keys(data1), keys(data2)):
        a = data1.get(k)
        b = data2.get(k)
        out[k] = merge(a, b)
    return out


@merge.register
def _(data1: list, data2: list):
    out = []
    m = min(len(data1), len(data2))
    for a, b in zip(data1[:m], data2[:m]):
        out.append(merge(a, b))
    if len(data1) > len(data2):
        out.extend(data1[m:])
    else:
        out.extend(data2[m:])
    return out


def diff(data1, data2):
    if is_object(data1) and is_object(data2):
        return _diff(data1, data2)
    if data1 is data2 or data1 == data2:
        return "no diff"
    else:
        return data2


def _diff(data1, data2):
    empty = type(data1)()
    if data1 is data2:
        return empty

    def red(acc, k):
        res = diff(get(data1, k, default=None), get(data2, k, default=None))
        if is_object(res) and is_empty(res) or res == "no diff":
            return acc
        return set(acc, [k], res)

    keys_ = union(keys(data1), keys(data2))
    return reduce(keys_, empty, red)


def information_paths(obj, path=()):
    if not is_object(obj):
        yield path
        return
    for k in keys(obj):
        yield from information_paths(obj[k], path + (k,))


def have_paths_in_common(diff1, diff2):
    try:
        next(intersection(information_paths(diff1), information_paths(diff2)))
    except StopIteration:
        return False
    return True
