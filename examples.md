# Examples

Real output from QueryCraft, captured from actual runs.

## Full query: columns, two conditions, ordering, limit

Command:

```bash
python3 querycraft.py --table products --columns "name,price" --where "price>10" --where "name LIKE %phone%" --order "price desc" --limit 5
```

Output:

```
SELECT name, price FROM products WHERE price > 10 AND name LIKE '%phone%' ORDER BY price DESC LIMIT 5;
```

## Bare minimum: just a table

Command:

```bash
python3 querycraft.py --table users
```

Output:

```
SELECT * FROM users;
```

## Quoting: numbers stay bare, text is quoted and escaped

Command:

```bash
python3 querycraft.py --table t --where "age>=21" --where "city=O'Brien"
```

Output:

```
SELECT * FROM t WHERE age >= 21 AND city = 'O''Brien';
```

Note how `21` is left unquoted (it parses as a number) while `O'Brien`
is wrapped in single quotes with its internal quote doubled — the
standard SQL way to escape a quote inside a string.
