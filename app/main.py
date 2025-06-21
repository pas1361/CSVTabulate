import csv
import argparse
import re
import operator
from tabulate import tabulate

OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

def avg(val) -> float:
    return sum(val) / len(val) if val else None

# расширение функционала - сумма значений
def total(val) -> float|int:
    return sum(val) if val else None

# расширение функционала - количество записей
def count(val) -> int:
    return len(val) if val else None

AGGREGATES = {
    'min': min,
    'max': max,
    'avg': avg,
    'sum': total, # расширение функционала - сумма значений
    'count': count # расширение функционала - количество записей
}

agg_keys_pattern = '|'.join(AGGREGATES.keys()) # функции для расширения возможных типов агрегаций собираются для парсинга регулярного выражения
# Новые функции добавляются только в словарь AGGREGATES, без необходимости вносить изменения где-либо ещё

def try_convert(val: str) -> float | str:
    try:
        return float(val)
    except ValueError:
        return val


def parse_where(expression: str) -> dict:
    reg = r'(\w+)\s*(=|!=|>=|<=|>|<)\s*(.+)'
    match = re.match(reg, expression)
    if not match:
        raise ValueError(f"Неправильный формат выражения для фильтрации: {expression}")
    key, op, val = match.groups()
    val = val.strip()
    try:
        val = float(val) if '.' in val else int(val)
    except ValueError:
        pass
    return {'key': key, 'operator': op, 'value': val}


def parse_aggregate(expression: str) -> dict:
    reg = rf'(\w+)\s*=\s*({agg_keys_pattern})'
    match = re.match(reg, expression)
    if not match:
        raise ValueError(f"Неправильный формат выражения для агрегации: {expression}")
    key, func = match.groups()
    return {'key': key, 'func': func}


def parse_order_by(expression: str) -> dict:
    reg = r'(\w+)\s*=\s*(asc|desc)'
    match = re.match(reg, expression)
    if not match:
        raise ValueError(f"Неправильный формат выражения для сортировки: {expression}")
    key, direction = match.groups()
    return {'key': key, 'reverse': direction.lower() == 'desc'}

def main():
    parser = argparse.ArgumentParser(description="CSVTabulate фильтрация, сортировка и агрегация")
    parser.add_argument("-f", "--file", type=str, required=True, help="Путь к CSV файлу")
    parser.add_argument("-w", "--where", type=str, help="Фильтрация. =|!=|>=|<=|>|< Например, rating>=4.5")
    parser.add_argument("-o", "--order-by", type=str, help="Сортировка. asc|desc Например, brand=asc или price=desc")
    parser.add_argument("-a", "--aggregate", type=str, help="Агрегация. min|max|avg|sum|count Например, rating=avg, price=max")
    args = parser.parse_args()


    with open(args.file, encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter = ",")
        data = list(reader)

    if args.where:
        where = parse_where(args.where)
        data = [
            row for row in data
            if OPERATORS[where['operator']](try_convert(row[where['key']]), where['value'])
        ]

    if args.order_by:
        order = parse_order_by(args.order_by)
        key = order['key']
        reverse = order['reverse']
        try:
            data.sort(key=lambda row: try_convert(row[key]), reverse=reverse)
        except KeyError:
            raise ValueError(f"Поле '{key}' не найдено в данных")

    if args.aggregate:
        agg = parse_aggregate(args.aggregate)
        key = agg['key']
        func = AGGREGATES[agg['func']]
        try:
            values = [float(row[key]) for row in data]
        except ValueError:
            raise ValueError(f"Поле {key} содержит нечисловые значения")
        if not values:
            print("Нет данных для агрегации.")
        else:
            result = func(values)
            # Вариант как в примере:
            print(tabulate([[result]], headers=[agg['func']], tablefmt="psql"))
            # Вариант с вертикальным отображением + заголовок:
            # print(tabulate([[agg['func']], [result]], headers=[key], tablefmt="psql", stralign='center'))
            # Вариант с горизонтальным отображением + заголовок:
            # print(tabulate([[key, agg['func'], result]], tablefmt="psql", stralign='center'))
    else:
        print(tabulate(data, headers='keys', tablefmt="psql"))

if __name__ == "__main__":
    main()