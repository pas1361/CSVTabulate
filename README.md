# CSVTabulate

**Тестовое задание выполнил Александр Первишко.**  
Удобный скрипт для работы с CSV-файлами: фильтрация строк, сортировка и вычисление агрегатов с выводом результата в красивой табличной форме.

## 📌 Описание

Этот инструмент позволяет:
- Фильтровать данные по условию (`--where`), например: `rating>=4.5`
- Сортировать данные по полю по возрастанию или убыванию (`--order-by`), например: `brand=asc` или `price=desc`
- Агрегировать по числовым полям (`--aggregate`): минимум, максимум, среднее, сумма, количество, например: `rating=avg`, `price=max`, `price=sum`, `rating=count`
- Выводить результаты в виде таблиц с помощью `tabulate`
- Простое расширение функций аггрегирования


## 🚀 Использование

```bash
python main.py -f path/to/file.csv [-w WHERE] [-o ORDER_BY] [-a AGGREGATE]
```

### Аргументы:

- `-f`, `--file` — путь к CSV-файлу (**обязательно**)
- `-w`, `--where` — фильтр, пример: `"rating>=4.5"`, `"brand!=apple"`, `"price<=600"`
- `-o`, `--order-by` — сортировка, пример: `"brand=asc"`, `"price=desc"`, `"rating=asc"`
- `-a`, `--aggregate` — агрегация, пример: `"rating=avg"`, `"price=max"`, `"price=avg"`, `"price=sum"`, `"price=count"`


## 📎 Примеры

### Фильтрация и вывод
Отфильтрует продукты с рейтингом не ниже 4.5 и выведет таблицу.

```bash
python main.py -f products.csv -w "rating>=4.5"
```
```
+------------------+---------+---------+----------+
| name             | brand   |   price |   rating |
|------------------+---------+---------+----------|
| iphone 15 pro    | apple   |     999 |      4.9 |
| galaxy s23 ultra | samsung |    1199 |      4.8 |
| redmi note 12    | xiaomi  |     199 |      4.6 |
| iphone 14        | apple   |     799 |      4.7 |
| galaxy z flip 5  | samsung |     999 |      4.6 |
| iphone 13 mini   | apple   |     599 |      4.5 |
+------------------+---------+---------+----------+
```

### Сортировка по цене
Отсортирует по цене по убыванию.

```bash
python main.py -f products.csv -o "price=desc"
```
```
+------------------+---------+---------+----------+
| name             | brand   |   price |   rating |
|------------------+---------+---------+----------|
| galaxy s23 ultra | samsung |    1199 |      4.8 |
| iphone 15 pro    | apple   |     999 |      4.9 |
| galaxy z flip 5  | samsung |     999 |      4.6 |
| iphone 14        | apple   |     799 |      4.7 |
| iphone 13 mini   | apple   |     599 |      4.5 |
| iphone se        | apple   |     429 |      4.1 |
| galaxy a54       | samsung |     349 |      4.2 |
| poco x5 pro      | xiaomi  |     299 |      4.4 |
| redmi note 12    | xiaomi  |     199 |      4.6 |
| redmi 10c        | xiaomi  |     149 |      4.1 |
+------------------+---------+---------+----------+
```

### Агрегация
Агрегация (минимум, максимум, среднее) (дополнительно: сумма и количество строк).
Выведет среднее значение цены по всему файлу.
```bash
python main.py -f products.csv -a "price=avg"
```
```
+-------+
|   avg |
|-------|
|   602 |
+-------+
```

### Комбинация фильтрации и сортировки
Фильтрует продукты с рейтингом 4.5 и выше, сортирует по бренду в алфавитном порядке по возрастанию.

```bash
python main.py -f products.csv -w "rating>=4.5" -o "brand=asc"
```
```
+------------------+---------+---------+----------+
| name             | brand   |   price |   rating |
|------------------+---------+---------+----------|
| iphone 15 pro    | apple   |     999 |      4.9 |
| iphone 14        | apple   |     799 |      4.7 |
| iphone 13 mini   | apple   |     599 |      4.5 |
| galaxy s23 ultra | samsung |    1199 |      4.8 |
| galaxy z flip 5  | samsung |     999 |      4.6 |
| redmi note 12    | xiaomi  |     199 |      4.6 |
+------------------+---------+---------+----------+
```

### Все опции вместе
Фильтрует продукты с рейтингом 4.5 и выше, сортирует по бренду по возрастанию, и выводит максимальную цену среди отфильтрованных.
```bash
python main.py -f products.csv -w "rating>=4.5" -o "brand=asc" -a "price=max"
```
```
+-------+
|   max |
|-------|
|  1199 |
+-------+
```
### Несколько видов вывода аггрегаций:
```
(.venv) PS C:\PythonProjects\CSVTabulate\app> python main.py -f products.csv -w "price<=599" -a "rating=max"
+-------+
|   max |
|-------|
|   4.6 |
+-------+
+----------+
|  rating  |
|----------|
|   max    |
|   4.6    |
+----------+
+--------+-----+-----+
| rating | max | 4.6 |
+--------+-----+-----+
```

## ✅ Результаты выполнения
```
(.venv) PS C:\PythonProjects\CSVTabulate\app>  python main.py -f products.csv
+------------------+---------+---------+----------+
| name             | brand   |   price |   rating |
|------------------+---------+---------+----------|
| iphone 15 pro    | apple   |     999 |      4.9 |
| galaxy s23 ultra | samsung |    1199 |      4.8 |
| redmi note 12    | xiaomi  |     199 |      4.6 |
| iphone 14        | apple   |     799 |      4.7 |
| galaxy a54       | samsung |     349 |      4.2 |
| poco x5 pro      | xiaomi  |     299 |      4.4 |
| iphone se        | apple   |     429 |      4.1 |
| galaxy z flip 5  | samsung |     999 |      4.6 |
| redmi 10c        | xiaomi  |     149 |      4.1 |
| iphone 13 mini   | apple   |     599 |      4.5 |
+------------------+---------+---------+----------+

(.venv) PS C:\PythonProjects\CSVTabulate\app>  python main.py -f products.csv -a "price=max"
+-------+
|   max |
|-------|
|  1199 |
+-------+

(.venv) PS C:\PythonProjects\CSVTabulate\app> python main.py -f products.csv -a "price=avg"
+-------+
|   avg |
|-------|
|   602 |
+-------+

(.venv) PS C:\PythonProjects\CSVTabulate\app> python main.py -f products.csv -a "price=sum"
+-------+
|   sum |
|-------|
|  6020 |
+-------+

(.venv) PS C:\PythonProjects\CSVTabulate\app> python main.py -f products.csv -a "price=count"
+---------+
|   count |
|---------|
|      10 |
+---------+


(.venv) PS C:\PythonProjects\CSVTabulate\app> python main.py -f products.csv -w "brand=apple" -a "price=count"
+---------+
|   count |
|---------|
|       4 |
+---------+


(.venv) PS C:\PythonProjects\CSVTabulate\app> python main.py -f products.csv -w "brand=apple" -a "price=sum"
+-------+
|   sum |
|-------|
|  2826 |
+-------+


(.venv) PS C:\PythonProjects\CSVTabulate\app>  python main.py -f products.csv -w "brand!=apple"
+------------------+---------+---------+----------+
| name             | brand   |   price |   rating |
|------------------+---------+---------+----------|
| galaxy s23 ultra | samsung |    1199 |      4.8 |
| redmi note 12    | xiaomi  |     199 |      4.6 |
| galaxy a54       | samsung |     349 |      4.2 |
| poco x5 pro      | xiaomi  |     299 |      4.4 |
| galaxy z flip 5  | samsung |     999 |      4.6 |
| redmi 10c        | xiaomi  |     149 |      4.1 |
+------------------+---------+---------+----------+

(.venv) PS C:\PythonProjects\CSVTabulate\app>  python main.py -f products.csv -w "brand!=apple" -o "rating=desc"
+------------------+---------+---------+----------+
| name             | brand   |   price |   rating |
|------------------+---------+---------+----------|
| galaxy s23 ultra | samsung |    1199 |      4.8 |
| redmi note 12    | xiaomi  |     199 |      4.6 |
| galaxy z flip 5  | samsung |     999 |      4.6 |
| poco x5 pro      | xiaomi  |     299 |      4.4 |
| galaxy a54       | samsung |     349 |      4.2 |
| redmi 10c        | xiaomi  |     149 |      4.1 |
+------------------+---------+---------+----------+


(.venv) PS C:\PythonProjects\CSVTabulate\app>  python main.py -f products.csv -o "rating=asc"
+------------------+---------+---------+----------+
| name             | brand   |   price |   rating |
|------------------+---------+---------+----------|
| iphone se        | apple   |     429 |      4.1 |
| redmi 10c        | xiaomi  |     149 |      4.1 |
| galaxy a54       | samsung |     349 |      4.2 |
| poco x5 pro      | xiaomi  |     299 |      4.4 |
| iphone 13 mini   | apple   |     599 |      4.5 |
| redmi note 12    | xiaomi  |     199 |      4.6 |
| galaxy z flip 5  | samsung |     999 |      4.6 |
| iphone 14        | apple   |     799 |      4.7 |
| galaxy s23 ultra | samsung |    1199 |      4.8 |
| iphone 15 pro    | apple   |     999 |      4.9 |
+------------------+---------+---------+----------+

(.venv) PS C:\PythonProjects\CSVTabulate\app>  python main.py -f products.csv -o "price=desc"
+------------------+---------+---------+----------+
| name             | brand   |   price |   rating |
|------------------+---------+---------+----------|
| galaxy s23 ultra | samsung |    1199 |      4.8 |
| iphone 15 pro    | apple   |     999 |      4.9 |
| galaxy z flip 5  | samsung |     999 |      4.6 |
| iphone 14        | apple   |     799 |      4.7 |
| iphone 13 mini   | apple   |     599 |      4.5 |
| iphone se        | apple   |     429 |      4.1 |
| galaxy a54       | samsung |     349 |      4.2 |
| poco x5 pro      | xiaomi  |     299 |      4.4 |
| redmi note 12    | xiaomi  |     199 |      4.6 |
| redmi 10c        | xiaomi  |     149 |      4.1 |
+------------------+---------+---------+----------+


(.venv) PS C:\PythonProjects\CSVTabulate\app> python main.py -f products.csv -o "name=asc"
+------------------+---------+---------+----------+
| name             | brand   |   price |   rating |
|------------------+---------+---------+----------|
| galaxy a54       | samsung |     349 |      4.2 |
| galaxy s23 ultra | samsung |    1199 |      4.8 |
| galaxy z flip 5  | samsung |     999 |      4.6 |
| iphone 13 mini   | apple   |     599 |      4.5 |
| iphone 14        | apple   |     799 |      4.7 |
| iphone 15 pro    | apple   |     999 |      4.9 |
| iphone se        | apple   |     429 |      4.1 |
| poco x5 pro      | xiaomi  |     299 |      4.4 |
| redmi 10c        | xiaomi  |     149 |      4.1 |
| redmi note 12    | xiaomi  |     199 |      4.6 |
+------------------+---------+---------+----------+


(.venv) PS C:\PythonProjects\CSVTabulate\app>  python main.py -f products.csv -w "brand=samsung"
+------------------+---------+---------+----------+
| name             | brand   |   price |   rating |
|------------------+---------+---------+----------|
| galaxy s23 ultra | samsung |    1199 |      4.8 |
| galaxy a54       | samsung |     349 |      4.2 |
| galaxy z flip 5  | samsung |     999 |      4.6 |
+------------------+---------+---------+----------+


(.venv) PS C:\PythonProjects\CSVTabulate\app>  python main.py -f products.csv -w "price<=599"
+----------------+---------+---------+----------+
| name           | brand   |   price |   rating |
|----------------+---------+---------+----------|
| redmi note 12  | xiaomi  |     199 |      4.6 |
| galaxy a54     | samsung |     349 |      4.2 |
| poco x5 pro    | xiaomi  |     299 |      4.4 |
| iphone se      | apple   |     429 |      4.1 |
| redmi 10c      | xiaomi  |     149 |      4.1 |
| iphone 13 mini | apple   |     599 |      4.5 |
+----------------+---------+---------+----------+

(.venv) PS C:\PythonProjects\CSVTabulate\app> python main.py -f products.csv -w "price<=599" -a "price=avg"
+---------+
|     avg |
|---------|
| 337.333 |
+---------+

(.venv) PS C:\PythonProjects\CSVTabulate\app> python main.py -f products.csv -w "price<=599" -a "rating=avg"
+---------+
|     avg |
|---------|
| 4.31667 |
+---------+

(.venv) PS C:\PythonProjects\CSVTabulate\app> python main.py -f products.csv -w "price<=599" -a "rating=max"
+-------+
|   max |
|-------|
|   4.6 |
+-------+

(.venv) PS C:\PythonProjects\CSVTabulate\app> python main.py -f products.csv -w "price<=599" -a "price=min"
+-------+
|   min |
|-------|
|   149 |
+-------+

(.venv) PS C:\PythonProjects\CSVTabulate\app> python main.py -f products.csv -w "price<=599" -a "price=count"
+---------+
|   count |
|---------|
|       6 |
+---------+

(.venv) PS C:\PythonProjects\CSVTabulate\app> python main.py -f products.csv -w "price<=599" -a "price=sum"
+-------+
|   sum |
|-------|
|  2024 |
+-------+
```

## 📄 Автор

Александр Первишко
