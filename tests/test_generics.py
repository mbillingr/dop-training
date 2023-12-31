from copy import deepcopy

from dop_game import generics as _


def test_get():
    assert _.get({"a": 1, "b": 2}, ["a"]) == 1
    assert _.get([10, 20, 30], [1]) == 20
    assert _.get([{}, {"a": 5, "b": [1, 2, 3]}, {}], [1, "b", 0]) == 1


def test_set():
    old = [{}, {"a": (5, 6), "b": [1, 2, 3]}, {}]
    original = deepcopy(old)

    new = _.set(old, [1, "a", 0], 42)

    # value was updated
    assert new == [{}, {"a": (42, 6), "b": [1, 2, 3]}, {}]

    # input was not mutated
    assert old == original

    # structural sharing
    assert new[0] is old[0]
    assert new[1]["b"] is old[1]["b"]


def test_set_new_field():
    old = {}
    original = deepcopy(old)

    new = _.set(old, "x", 42)

    # value was updated
    assert new == {"x": 42}

    # input was not mutated
    assert old == original


def test_map():
    assert _.map([], ident) == []
    assert _.map((), ident) == ()
    assert _.map(set(), ident) == set()
    assert _.map({}, ident) == {}

    assert _.map([1, 2, 3], ident) == [1, 2, 3]
    assert _.map([4, 5, 6], str) == ["4", "5", "6"]

    assert _.map({"a": "b", "c": "d"}, str.upper) == {"a": "B", "c": "D"}


def test_filter():
    assert _.filter([], lambda: True) == []
    assert _.filter((), lambda: True) == ()
    assert _.filter(set(), lambda: True) == set()
    assert _.filter({}, lambda: True) == {}

    assert _.filter([1, 2, 3, 4], lambda x: x % 2 == 0) == [2, 4]
    assert _.filter({"a": 1, "c": 2}, lambda x: x % 2 == 0) == {"c": 2}


def test_sum():
    assert _.sum([]) == 0
    assert _.sum([1, 2, 3]) == 6
    assert _.sum({"a": 4, "b": 5}) == 9
    assert _.sum(["a", "b", "c"], "x") == "xabc"


def test_merge():
    assert _.merge({}, {}) == {}
    assert _.merge([], []) == []

    assert _.merge({"a": 1}, {}) == {"a": 1}
    assert _.merge({}, {"a": 1}) == {"a": 1}
    assert _.merge({"a": 1}, {"a": 2}) == {"a": 2}
    assert _.merge({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}

    assert _.merge([1], []) == [1]
    assert _.merge([], [1]) == [1]
    assert _.merge([1], [2]) == [2]
    assert _.merge([1], [None, 2]) == [1, 2]

    assert _.merge({"a": [{}, {}]}, {"a": [{"x": 1}]}) == {"a": [{"x": 1}, {}]}


def test_diff_dict():
    assert _.diff({"a": 1}, {"a": 1}) == {}
    assert _.diff({"a": 1}, {"a": 2}) == {"a": 2}
    assert _.diff({"a": 1}, {"a": 1, "b": 2}) == {"b": 2}
    # assert _.diff({"a": 1, "b": 2}, {"a": 1}) == not supported


def test_diff_nested_dict():
    assert _.diff({"a": {"x": 1}}, {"a": {"x": 2}}) == {"a": {"x": 2}}
    assert _.diff({"a": {"x": 1}}, {"a": {"x": 1, "y": 2}}) == {"a": {"y": 2}}
    # assert _.diff({"a": {"x": 1, "y": 2}}, {"a": {"x": 1}}) == not supported


def test_diff_array():
    assert _.diff([1], [1]) == []
    assert _.diff([1], [2]) == [2]
    assert _.diff([1], [1, 2]) == [None, 2]


def test_diff():
    original = {
        "catalog": {
            "books_by_isbn": {
                "978-1779501127": {
                    "isbn": "978-1779501127",
                    "title": "Watchmen",
                    "publication_year": 1987,
                }
            }
        },
        "authors_by_id": {
            "alan-moore": {"name": "Alan Moore", "book_isbns": ["978-1779501127"]},
            "dave-gibbons": {
                "name": "Dave Gibbons",
                "book_isbns": ["978-1779501127"],
            },
        },
    }

    new_title_and_author = _.set(
        _.set(
            original,
            ["catalog", "books_by_isbn", "978-1779501127", "title"],
            "The Watchmen",
        ),
        ["authors_by_id", "dave-gibbons", "name"],
        "David Chester Gibbons",
    )

    new_year = _.set(
        original,
        ["catalog", "books_by_isbn", "978-1779501127", "publication_year"],
        1986,
    )

    assert _.diff(original, new_year) == {
        "catalog": {
            "books_by_isbn": {
                "978-1779501127": {
                    "publication_year": 1986,
                }
            }
        }
    }

    assert _.diff(original, new_title_and_author) == {
        "catalog": {
            "books_by_isbn": {
                "978-1779501127": {
                    "title": "The Watchmen",
                }
            }
        },
        "authors_by_id": {"dave-gibbons": {"name": "David Chester Gibbons"}},
    }

    assert list(_.information_paths(_.diff(original, new_year))) == [
        ("catalog", "books_by_isbn", "978-1779501127", "publication_year")
    ]

    assert list(_.information_paths(_.diff(original, new_title_and_author))) == [
        ("catalog", "books_by_isbn", "978-1779501127", "title"),
        ("authors_by_id", "dave-gibbons", "name"),
    ]


def ident(x):
    return x
