

from typing import List

from parquet_airflow.schemas.connection_schema import ConnectionSchema
from parquet_airflow.schemas.parquet_jobs_schema import ParquetJobSchema
from core.db_connector import DatabaseClient


class ParquetModel:

	@classmethod
	def get_active_jobs(cls, configDb:ConnectionSchema)->List[ParquetJobSchema]:
		query = '''SELECT 
					pj.job_id,
					pj.job_name,
					pj.database_name,
					pj.connection_id,
					pj.query_text,
					pj.output_file,
					pj.cron_job,
					pj.run_once_at,
					pj.is_active,
					pj.last_run_at,
					pj.next_run_at,
					pj.is_dynamic_date,
					pj.params_dynamics,
					pj.created_at,
					pj.updated_at,
					cs.engine,
					cs.username,
					cs."password",
					cs.host,
					cs.port
				FROM tasks.parquet_jobs pj
				LEFT JOIN tasks.connection_sources cs
					ON cs.connection_id = pj.connection_id
				WHERE pj.is_active IS true'''
		reponse = DatabaseClient(configDb).select_all(query)
		return [ParquetJobSchema.from_dict(row) for row in reponse] if len(reponse) > 0 else []
	
