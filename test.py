import time
import traceback
from datetime import datetime

import pandas as pd

from sqlalchemy import create_engine, text

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger

from concurrent.futures import ThreadPoolExecutor


# ==========================================
# CONEXION POSTGRESQL
# ==========================================

DATABASE_URL = (
    "postgresql://postgres:password@localhost:5432/testdb"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# ==========================================
# SCHEDULER
# ==========================================

scheduler = BackgroundScheduler(
    executors={
        "default": ThreadPoolExecutor(10)
    }
)

scheduler.start()


# ==========================================
# CACHE JOBS
# ==========================================

jobs_cache = {}


# ==========================================
# GUARDAR LOGS
# ==========================================

def guardar_log(
    job_id,
    inicio,
    fin,
    status,
    mensaje=None,
    error=None
):

    with engine.begin() as conn:

        conn.execute(text("""
            INSERT INTO job_logs (
                job_id,
                inicio,
                fin,
                status,
                mensaje,
                error
            )
            VALUES (
                :job_id,
                :inicio,
                :fin,
                :status,
                :mensaje,
                :error
            )
        """), {
            "job_id": job_id,
            "inicio": inicio,
            "fin": fin,
            "status": status,
            "mensaje": mensaje,
            "error": error
        })


# ==========================================
# EJECUTAR JOB
# ==========================================

def ejecutar_job(job_id):

    inicio = datetime.now()

    try:

        with engine.begin() as conn:

            # Lock para evitar doble ejecución
            lock = conn.execute(text("""
                SELECT pg_try_advisory_lock(:id)
            """), {
                "id": job_id
            }).scalar()

            if not lock:
                print(f"Job {job_id} ya ejecutándose")
                return

            job = conn.execute(text("""
                SELECT *
                FROM jobs
                WHERE id = :id
            """), {
                "id": job_id
            }).mappings().first()

            if not job:
                return

            config = job["configuracion"]

            print(f"\nEjecutando job: {job['nombre']}")

            query = config["query"]

            result = conn.execute(
                text(query)
            )

            rows = result.fetchall()

            # Ejemplo convertir a DataFrame
            df = pd.DataFrame(rows)

            output = config.get("output")

            if output == "console":

                print(df)

            elif output == "csv":

                path = config["path"]

                df.to_csv(
                    path,
                    index=False
                )

                print(f"CSV generado: {path}")

            conn.execute(text("""
                UPDATE jobs
                SET ultima_ejecucion = NOW()
                WHERE id = :id
            """), {
                "id": job_id
            })

            guardar_log(
                job_id=job_id,
                inicio=inicio,
                fin=datetime.now(),
                status="SUCCESS",
                mensaje="Job ejecutado correctamente"
            )

    except Exception:

        error = traceback.format_exc()

        print(error)

        guardar_log(
            job_id=job_id,
            inicio=inicio,
            fin=datetime.now(),
            status="ERROR",
            error=error
        )


# ==========================================
# CREAR TRIGGER
# ==========================================

def construir_trigger(
    trigger_type,
    trigger_value
):

    # --------------------------------------
    # CRON
    # --------------------------------------

    if trigger_type == "cron":

        minute, hour, day, month, dow = (
            trigger_value.split()
        )

        return CronTrigger(
            minute=minute,
            hour=hour,
            day=day,
            month=month,
            day_of_week=dow
        )

    # --------------------------------------
    # INTERVAL
    # --------------------------------------

    elif trigger_type == "interval":

        seconds = int(trigger_value)

        return IntervalTrigger(
            seconds=seconds
        )

    # --------------------------------------
    # DATE
    # --------------------------------------

    elif trigger_type == "date":

        fecha = datetime.fromisoformat(
            trigger_value
        )

        return DateTrigger(
            run_date=fecha
        )

    else:

        raise Exception(
            f"Trigger inválido: {trigger_type}"
        )


# ==========================================
# CARGAR JOBS
# ==========================================

def cargar_jobs():

    with engine.begin() as conn:

        rows = conn.execute(text("""
            SELECT *
            FROM jobs
            WHERE activo = TRUE
        """)).mappings().all()

    for row in rows:

        job_id = row["id"]

        actualizado = str(
            row["actualizado_en"]
        )

        cache_key = (
            f"{job_id}_{actualizado}"
        )

        # Ya cargado
        if jobs_cache.get(job_id) == cache_key:
            continue

        # Eliminar job anterior
        try:
            scheduler.remove_job(
                str(job_id)
            )
        except:
            pass

        trigger = construir_trigger(
            row["trigger_type"],
            row["trigger_value"]
        )

        scheduler.add_job(
            ejecutar_job,
            trigger=trigger,
            args=[job_id],
            id=str(job_id),
            replace_existing=True
        )

        jobs_cache[job_id] = cache_key

        print(
            f"Job cargado: {row['nombre']}"
        )


# ==========================================
# LOOP PRINCIPAL
# ==========================================

print("Scheduler iniciado")

while True:

    try:

        cargar_jobs()

    except Exception as e:

        print(e)

    time.sleep(30)