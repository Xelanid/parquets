from contextlib import contextmanager
from typing import Any, Dict, List, Optional

import psycopg2
import pyodbc

from parquet_airflow import _ENV
from parquet_airflow.schemas.connection_schema import ConnectionSchema


class DatabaseClient:
    """	Cliente para conectarse a PostgreSQL o SQL Server y ejecutar consultas parametrizadas."""

    def __init__(self, config:ConnectionSchema):
        self.engine     = config.engine.lower()
        self.config     = config
        self.connection = None

    def connect(self):
        if self.engine == "postgres":
            self.connection = psycopg2.connect(
                host     = self.config.host,
                port     = self.config.port,
                dbname   = self.config.databaseName,
                user     = self.config.username,
                password = self.config.password,
            )
        elif self.engine == "sqlserver":
            conn_str = (
                "DRIVER={ODBC Driver 18 for SQL Server};"
                f"SERVER={self.config.host},{self.config.port};"
                f"DATABASE={self.config.databaseName};"
                f"UID={self.config.username};"
                f"PWD={self.config.password};"
                "TrustServerCertificate=yes;"
            )
            self.connection = pyodbc.connect(conn_str)
        else:
            raise ValueError(f"Engine not supported: {self.engine}")
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    @contextmanager
    def cursor(self):
        if self.connection is None:
            self.connect()

        cur = self.connection.cursor()
        try:
            yield cur
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cur.close()

    def execute(self, query: str, params: Optional[Dict[str, Any]] = None) -> int:
        """
        Ejecuta INSERT, UPDATE, DELETE o comandos DDL.
        Retorna cantidad de filas afectadas.
        """
        params = params or {}

        with self.cursor() as cur:
            if len(params) > 0:
                cur.execute(query, params)
            else:
                cur.execute(query)
            return cur.rowcount

    def select_all(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Ejecuta SELECT y retorna lista de diccionarios.
        """
        params = params or {}

        with self.cursor() as cur:
            if len(params) > 0:
                cur.execute(query, params)
            else:
                cur.execute(query)
            columns = [col[0] for col in cur.description]
            rows = cur.fetchall()
            return [dict(zip(columns, row)) for row in rows]

    def select_one(self, query: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Ejecuta SELECT y retorna un solo registro.
        """
        params = params or {}
        with self.cursor() as cur:
            if len(params) > 0:
                cur.execute(query, params)
            else:
                cur.execute(query)
            row = cur.fetchone()
            if row is None:
                return None
            columns = [col[0] for col in cur.description]
            return dict(zip(columns, row))

    def execute_many_dynamic(self, query: str, params_list: List[Dict[str, Any]]) -> int:
        """
        Ejecuta la misma query varias veces con distintos parámetros.
        """
        total_rows = 0
        with self.cursor() as cur:
            for params in params_list:
                cur.execute(query, params)
                total_rows += cur.rowcount
        return