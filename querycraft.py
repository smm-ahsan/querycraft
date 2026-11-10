#!/usr/bin/env python3
"""QueryCraft - build a SQL SELECT statement from parts.

Builds (does not run) a single-line SELECT statement from command-line
pieces: table, columns, WHERE conditions, ORDER BY and LIMIT. Values
that parse as numbers are left unquoted; everything else is wrapped in
single quotes with internal single quotes doubled.

Standard library only.
"""

import argparse
import sys

# Longest first so ">=" wins over ">" and "<=" wins over "<".
OPERATORS = ["LIKE", "!=", ">=", "<=", "=", ">", "<"]


def parse_where(raw):
    """Parse 'field<op>value' into (field, op, value) or None if malformed."""
    for op in OPERATORS:
        idx = raw.find(op)
        if idx > 0:
            field = raw[:idx].strip()
            value = raw[idx + len(op):].strip()
            if field and value:
                return field, op, value
    return None


def quote_value(value):
    """Leave ints/floats bare; single-quote everything else, doubling quotes."""
    try:
        int(value)
        return value
    except ValueError:
        pass
    try:
        float(value)
        return value
    except ValueError:
        pass
    return "'" + value.replace("'", "''") + "'"


def build_query(args):
    columns = ", ".join(c.strip() for c in args.columns.split(",") if c.strip())
    if not columns:
        columns = "*"
    parts = ["SELECT", columns, "FROM", args.table]

    if args.where:
        conditions = []
        for raw in args.where:
            parsed = parse_where(raw)
            if parsed is None:
                return None, (
                    "error: malformed --where %r "
                    "(expected 'field<op>value', op one of =, !=, >=, <=, >, <, LIKE)"
                    % raw
                )
            field, op, value = parsed
            conditions.append("%s %s %s" % (field, op, quote_value(value)))
        parts += ["WHERE", " AND ".join(conditions)]

    if args.order:
        tokens = args.order.split()
        if len(tokens) == 1:
            parts += ["ORDER BY", tokens[0]]
        elif len(tokens) == 2 and tokens[1].lower() in ("asc", "desc"):
            parts += ["ORDER BY", "%s %s" % (tokens[0], tokens[1].upper())]
        else:
            return None, (
                "error: malformed --order %r (expected 'field' or 'field asc|desc')"
                % args.order
            )

    statement = " ".join(parts)
    if args.limit is not None:
        statement += " LIMIT %d" % args.limit
    statement += ";"
    return statement, None


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="querycraft.py",
        description="Build a SQL SELECT statement from parts (does not run it).",
    )
    parser.add_argument("--table", required=True, help="Table name (required).")
    parser.add_argument(
        "--columns",
        default="*",
        help="Comma-separated column list (default: *).",
    )
    parser.add_argument(
        "--where",
        action="append",
        default=[],
        metavar="COND",
        help="Condition 'field<op>value'; repeatable. Operators: =, !=, >=, <=, >, <, LIKE.",
    )
    parser.add_argument(
        "--order",
        default=None,
        help="Ordering: 'field', 'field asc' or 'field desc'.",
    )
    parser.add_argument("--limit", default=None, help="Row limit (integer).")
    args = parser.parse_args(argv)

    if args.limit is not None:
        try:
            args.limit = int(args.limit)
        except ValueError:
            print(
                "error: --limit must be an integer, got %r" % args.limit,
                file=sys.stderr,
            )
            return 2
        if args.limit < 0:
            print("error: --limit must not be negative", file=sys.stderr)
            return 2

    statement, error = build_query(args)
    if error:
        print(error, file=sys.stderr)
        return 2
    print(statement)
    return 0


if __name__ == "__main__":
    sys.exit(main())
