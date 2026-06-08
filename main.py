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
        


		