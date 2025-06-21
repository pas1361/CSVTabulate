import pytest
import csv
from io import StringIO
from unittest.mock import patch, mock_open
from main import (
    OPERATORS,
    avg,
    total,
    count,
    try_convert,
    parse_where,
    parse_aggregate,
    parse_order_by,
)

TEST_CSV_DATA = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
iphone 14,apple,799,4.7
galaxy a54,samsung,349,4.2
poco x5 pro,xiaomi,299,4.4
iphone se,apple,429,4.1
galaxy z flip 5,samsung,999,4.6
redmi 10c,xiaomi,149,4.1
iphone 13 mini,apple,599,4.5
"""

@pytest.fixture
def sample_data():
    with StringIO(TEST_CSV_DATA) as f:
        reader = csv.DictReader(f)
        return list(reader)


def test_try_convert():
    assert try_convert("123") == 123
    assert try_convert("123.45") == 123.45
    assert try_convert("abc") == "abc"
    assert try_convert("") == ""
    assert try_convert("-4.5") == -4.5
    assert try_convert("0") == 0


def test_avg():
    assert avg([1, 2, 3, 4, 5]) == 3.0
    assert avg([]) is None
    assert avg([1.5, 2.5, 3.5]) == 2.5
    assert avg([10]) == 10.0
    assert avg([-1, 0, 1]) == 0.0


def test_count():
    assert count([1, 2, 3, 4, 5]) == 5
    assert count([]) is None
    assert count([1.5, -2.5, 0, 3.5]) == 4
    assert count([-10]) == 1
    assert count([-1, 0, 1]) == 3
    assert count(['dfg', 0, -1, '123']) == 4
    assert count(OPERATORS) == 6


def test_total():
    assert total([1, 2, 3, 4, 5]) == 15
    assert total([]) is None
    assert total([1.5, -2.5, 0, 3.5]) == 2.5
    assert total([-10]) == -10.0
    assert total([-1, 0, 1]) == 0


def test_parse_where():
    assert parse_where("price>100") == {'key': 'price', 'operator': '>', 'value': 100}
    assert parse_where("rating>=4.5") == {'key': 'rating', 'operator': '>=', 'value': 4.5}
    assert parse_where("brand=apple") == {'key': 'brand', 'operator': '=', 'value': 'apple'}
    assert parse_where("name!=test") == {'key': 'name', 'operator': '!=', 'value': 'test'}
    assert parse_where("price<=500") == {'key': 'price', 'operator': '<=', 'value': 500}


def test_parse_aggregate():
    assert parse_aggregate("price=avg") == {'key': 'price', 'func': 'avg'}
    assert parse_aggregate("rating=max") == {'key': 'rating', 'func': 'max'}
    assert parse_aggregate("price=sum") == {'key': 'price', 'func': 'sum'}
    assert parse_aggregate("rating=min") == {'key': 'rating', 'func': 'min'}
    assert parse_aggregate("name=count") == {'key': 'name', 'func': 'count'}

    with pytest.raises(ValueError, match="Неправильный формат выражения для агрегации"):
        parse_aggregate("price=")
    with pytest.raises(ValueError):
        parse_aggregate("=avg")
    with pytest.raises(ValueError):
        parse_aggregate("price=unknown")
    with pytest.raises(ValueError):
        parse_aggregate("")
    with pytest.raises(ValueError):
        parse_aggregate("invalid")


def test_parse_order_by():
    assert parse_order_by("price=asc") == {'key': 'price', 'reverse': False}
    assert parse_order_by("rating=desc") == {'key': 'rating', 'reverse': True}
    assert parse_order_by("name=asc") == {'key': 'name', 'reverse': False}
    assert parse_order_by("brand=desc") == {'key': 'brand', 'reverse': True}

    with pytest.raises(ValueError, match="Неправильный формат выражения для сортировки"):
        parse_order_by("price=")
    with pytest.raises(ValueError):
        parse_order_by("=asc")
    with pytest.raises(ValueError):
        parse_order_by("price=invalid")
    with pytest.raises(ValueError):
        parse_order_by("")
    with pytest.raises(ValueError):
        parse_order_by("invalid expression")


def test_filter_data(sample_data):
    filtered = [row for row in sample_data
                if OPERATORS['='](row['brand'], 'apple')]
    assert len(filtered) == 4
    assert all(row['brand'] == 'apple' for row in filtered)

    filtered = [row for row in sample_data
                if OPERATORS['>='](float(row['rating']), 4.5)]
    assert len(filtered) == 6
    assert all(float(row['rating']) >= 4.5 for row in filtered)

    filtered = [row for row in sample_data
                if OPERATORS['<'](float(row['price']), 500)]
    assert len(filtered) == 5
    assert all(float(row['price']) < 500 for row in filtered)


def test_sort_data(sample_data):
    sorted_data = sorted(sample_data, key=lambda row: float(row['price']))
    assert float(sorted_data[0]['price']) == 149
    assert float(sorted_data[-1]['price']) == 1199

    sorted_data = sorted(sample_data, key=lambda row: float(row['rating']), reverse=True)
    assert float(sorted_data[0]['rating']) == 4.9
    assert float(sorted_data[-1]['rating']) == 4.1

    sorted_data = sorted(sample_data, key=lambda row: row['name'])
    assert sorted_data[0]['name'].startswith('galaxy a54')
    assert sorted_data[-1]['name'].startswith('redmi')


def test_aggregate_data(sample_data):
    prices = [float(row['price']) for row in sample_data]
    ratings = [float(row['rating']) for row in sample_data]
    names = [row['name'] for row in sample_data]

    assert min(prices) == 149
    assert max(prices) == 1199
    assert avg(prices) == sum(prices) / len(prices)
    assert total(prices) == sum(prices)
    assert count(prices) == len(prices)

    assert min(ratings) == 4.1
    assert max(ratings) == 4.9
    assert count(names) == len(names)


@patch('sys.argv', ['main.py', '-f', 'products.csv'])
@patch('builtins.open', mock_open(read_data=TEST_CSV_DATA))
def test_main_no_args(capsys):
    from main import main
    main()
    captured = capsys.readouterr()
    assert "iphone 15 pro" in captured.out
    assert "galaxy s23 ultra" in captured.out
    assert "redmi note 12" in captured.out
    assert len(captured.out.splitlines()) == 14  # 10 строк + заголовок 3 + нижняя граница 1


@patch('sys.argv', ['main.py', '-f', 'products.csv', '-w', 'brand=apple'])
@patch('builtins.open', mock_open(read_data=TEST_CSV_DATA))
def test_main_with_where(capsys):
    from main import main
    main()
    captured = capsys.readouterr()
    output = captured.out
    assert "iphone 15 pro" in output
    assert "galaxy s23 ultra" not in output
    assert "apple" in output
    assert "samsung" not in output
    assert len(output.splitlines()) == 8  # 4 apple продукта + заголовок 3 + нижняя граница 1


@patch('sys.argv', ['main.py', '-f', 'products.csv', '-o', 'price=asc'])
@patch('builtins.open', mock_open(read_data=TEST_CSV_DATA))
def test_main_with_order_by(capsys):
    from main import main
    main()
    captured = capsys.readouterr()
    lines = captured.out.splitlines()
    assert "redmi 10c" in lines[3]  # Должен быть первым после заголовков (самый дешевый)
    assert "galaxy s23 ultra" in lines[-2]  # Должен быть последним (самый дорогой)


@patch('sys.argv', ['main.py', '-f', 'products.csv', '-a', 'price=avg'])
@patch('builtins.open', mock_open(read_data=TEST_CSV_DATA))
def test_main_with_aggregate(capsys):
    from main import main
    main()
    captured = capsys.readouterr()
    expected_avg = 602.0


@patch('sys.argv', ['main.py', '-f', 'products.csv', '-a', 'price=min'])
@patch('builtins.open', mock_open(read_data=TEST_CSV_DATA))
def test_main_with_aggregate(capsys):
    from main import main
    main()
    captured = capsys.readouterr()
    expected_avg = 149