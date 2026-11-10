# QueryCraft

Build a correct SQL SELECT statement from simple command-line parts.

QueryCraft **builds** SQL — it does not run it. It never connects to a
database. It is a drafting and learning tool: handy when you are sketching
a query, learning how SELECT statements fit together, or generating SQL
text to paste into your own database client.

Supported WHERE operators: `=`, `!=`, `>=`, `<=`, `>`, `<`, `LIKE`.
Values that parse as an int or float are left unquoted; everything else
is wrapped in single quotes with any internal single quote doubled.

## Requirements

- Python 3
- Standard library only — nothing to install

## Usage

```
python3 querycraft.py --table TABLE [--columns "a,b"] [--where "field<op>value"]...
                      [--order "field [asc|desc]"] [--limit N]
```

- `--table` (required): the table name.
- `--columns`: comma-separated column list, default `*`.
- `--where`: one condition per flag, repeatable. Conditions are joined
  with `AND`. Format: `field<op>value`, e.g. `price>10`, `age>=21`,
  `name LIKE %phone%`.
- `--order`: `field`, `field asc` or `field desc`.
- `--limit`: integer row limit.

Malformed `--where` conditions and a non-integer `--limit` exit with
code 2 and a clear error message.

### Examples

```bash
python3 querycraft.py --table products --columns "name,price" --where "price>10" --where "name LIKE %phone%" --order "price desc" --limit 5
# SELECT name, price FROM products WHERE price > 10 AND name LIKE '%phone%' ORDER BY price DESC LIMIT 5;

python3 querycraft.py --table users
# SELECT * FROM users;

python3 querycraft.py --table t --where "age>=21" --where "city=O'Brien"
# SELECT * FROM t WHERE age >= 21 AND city = 'O''Brien';
```

See `examples.md` for full captured runs.

## License

MIT — see `LICENSE`.
