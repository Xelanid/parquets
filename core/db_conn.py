import psycopg2
import pyodbc


def conectar_postgres(conn_data):
    return psycopg2.connect(
        host=conn_data["host"],
        port=conn_data["puerto"],
        dbname=conn_data["base_datos"],
        user=conn_data["usuario"],
        password=conn_data["password"]
    )


def conectar_sqlserver(conn_data):
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={conn_data['host']},{conn_data['puerto']};"
        f"DATABASE={conn_data['base_datos']};"
        f"UID={conn_data['usuario']};"
        f"PWD={conn_data['password']};"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)


def obtener_conexion(conn_data):
    motor = conn_data["motor"].lower()

    if motor == "postgres":
        return conectar_postgres(conn_data)

    if motor == "sqlserver":
        return conectar_sqlserver(conn_data)

    raise ValueError(f"Motor no soportado: {motor}")


def ejecutar_query(conn_data, sql_text, parametros):
    with obtener_conexion(conn_data) as conn:
        with conn.cursor() as cur:
            cur.execute(sql_text, parametros)

            columnas = [desc[0] for desc in cur.description]
            registros = cur.fetchall()

            return [
                dict(zip(columnas, fila))
                for fila in registros
            ]