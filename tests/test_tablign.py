import pytest

import tablign


def test_plain():
    data = """A  1.34  -214.1\nCCCC 55.534 1131.1"""
    ref = """A     1.34  -214.1\nCCCC 55.534 1131.1"""
    assert tablign.tablign(data) == ref


@pytest.mark.parametrize("sep_char", [","])
def test_column_seps(sep_char):
    data = """A  {} 1.34    {} -214.1
    CCCC {}        55.534 {} 1131.1""".format(
        *(4 * sep_char)
    )
    ref = """A    {}  1.34  {} -214.1
CCCC {} 55.534 {} 1131.1""".format(
        *(4 * sep_char)
    )
    assert tablign.tablign(data) == ref


def test_empty_cell():
    data = "| A   |  B |\n||C|"
    ref = "| A | B |\n|   | C |"
    print("repr", repr(tablign.tablign(data)))
    assert tablign.tablign(data) == ref


def test_different_column_lengths():
    data = "| A   |  B |\n|C|"
    ref = "| A | B |\n| C |   |"
    assert tablign.tablign(data) == ref


def test_csv():
    data = """A,B,\nCCCC,,"""
    ref = """A    , B ,\nCCCC ,   ,"""
    assert tablign.tablign(data) == ref


def test_first_column_missing():
    data = "A,B,Z\n      ,C,Z"
    ref = "A , B , Z\n  , C , Z"
    assert tablign.tablign(data) == ref


def test_col_types():
    data = """1,A,B,121.32,89,4.5E+11,ABCD\n2,C,D,24.1,1234,10.0E+2,AB"""
    ref = """1 , A , B , 121.32 ,   89 ,  4.5E+11 , ABCD\n2 , C , D ,  24.1  , 1234 , 10.0E+2  , AB  """
    print(data)
    print(ref)
    print(tablign.tablign(data))
    assert tablign.tablign(data) == ref


if __name__ == "__main__":
    test_column_seps(",")
