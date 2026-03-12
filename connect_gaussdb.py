#!/usr/bin/env python3
"""Simple GaussDB connection script.

Usage examples:
  python connect_gaussdb.py --host 127.0.0.1 --port 8000 --user dbuser --password secret --database postgres

Or use environment variables:
  export GAUSSDB_HOST=127.0.0.1
  export GAUSSDB_PORT=8000
  export GAUSSDB_USER=dbuser
  export GAUSSDB_PASSWORD=secret
  export GAUSSDB_DATABASE=postgres
  python connect_gaussdb.py
"""

from __future__ import annotations

import argparse
import os
import sys

try:
    import psycopg2
except ImportError as exc:  # pragma: no cover - import guard for runtime usage
    print(
        "Missing dependency: psycopg2.\n"
        "Install it with:\n"
        "  pip install psycopg2-binary",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Connect to GaussDB and run a simple validation query.",
    )
    parser.add_argument("--host", default=os.getenv("GAUSSDB_HOST"), help="GaussDB host")
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("GAUSSDB_PORT", "8000")),
        help="GaussDB port, default: 8000",
    )
    parser.add_argument("--user", default=os.getenv("GAUSSDB_USER"), help="Database user")
    parser.add_argument(
        "--password",
        default=os.getenv("GAUSSDB_PASSWORD"),
        help="Database password",
    )
    parser.add_argument(
        "--database",
        default=os.getenv("GAUSSDB_DATABASE"),
        help="Database name",
    )
    parser.add_argument(
        "--sslmode",
        default=os.getenv("GAUSSDB_SSLMODE", "prefer"),
        help="SSL mode, for example disable / require / verify-ca / verify-full",
    )
    parser.add_argument(
        "--connect-timeout",
        type=int,
        default=int(os.getenv("GAUSSDB_CONNECT_TIMEOUT", "10")),
        help="Connection timeout in seconds",
    )
    return parser


def validate_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    missing = [
        name
        for name in ("host", "user", "database")
        if not getattr(args, name)
    ]
    if missing:
        parser.error(
            "Missing required connection fields: "
            + ", ".join(missing)
            + ". Provide them via CLI arguments or GAUSSDB_* environment variables."
        )


def connect_and_query(args: argparse.Namespace) -> int:
    connection_kwargs = {
        "host": args.host,
        "port": args.port,
        "user": args.user,
        "dbname": args.database,
        "connect_timeout": args.connect_timeout,
        "application_name": "gaussdb_python_client",
    }

    if args.password:
        connection_kwargs["password"] = args.password
    if args.sslmode:
        connection_kwargs["sslmode"] = args.sslmode

    try:
        with psycopg2.connect(**connection_kwargs) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        version(),
                        current_database(),
                        current_schema(),
                        current_user
                    """
                )
                version, database_name, schema_name, current_user = cursor.fetchone()

        print("GaussDB connection succeeded.")
        print(f"database      : {database_name}")
        print(f"schema        : {schema_name}")
        print(f"user          : {current_user}")
        print(f"server version: {version}")
        return 0
    except psycopg2.Error as exc:
        print("GaussDB connection failed.", file=sys.stderr)
        print(f"error type    : {exc.__class__.__name__}", file=sys.stderr)
        print(f"error message : {exc}", file=sys.stderr)
        return 1


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    validate_args(args, parser)
    return connect_and_query(args)


if __name__ == "__main__":
    raise SystemExit(main())
