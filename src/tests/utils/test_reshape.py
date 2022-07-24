"""Unit tests for reshape util functions"""
from networkft.utils.reshape import flatten_dict


def test_flatten():
    test_dictionary = {
        "root": {"test_1": [0, 1], "test_2": {"1": 1, "2": "a"}},
        "root_2": {"test_3": "b"},
    }

    expected_dictionary = {
        "root": {"test_1": [0, 1], "test_2": {"1": 1, "2": "a"}},
        "root.test_1": [0, 1],
        "root.test_2": {"1": 1, "2": "a"},
        "root.test_2.1": 1,
        "root.test_2.2": "a",
        "root_2": {"test_3": "b"},
        "root_2.test_3": "b",
    }

    dictionary = flatten_dict(test_dictionary)
    assert dictionary == expected_dictionary
