import pytest

def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Dzielenie przez Zero")
    return a / b

def test_addition():
    result = add(2.5, 3.5)
    assert result == 6
    assert result == 6.0

def test_division():
    assert  divide(5, 1) == 5
    assert  divide(5, 1) == 5.0

def test_division_by_two():
    assert divide(6, 2) == 3
    assert divide(6, 2) == 3.0

def test_divisine_by_zero():
    with pytest.raises(ZeroDivisionError):
        assert divide(10, 0)

def test_division_type():
    assert divide(6, "2")

def test_division_type_error():
    with pytest.raises(TypeError):
        assert divide(6, "2")

