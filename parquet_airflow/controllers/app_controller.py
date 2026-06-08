


from datetime import datetime, timedelta

from parquet_airflow import _ENV
from parquet_airflow.models.parquet_pg_model import ParquetModel
from parquet_airflow.schemas.connection_schema import ConnectionSchema
from parquet_airflow.utils.format_query_util import QueryParamTransformer
from core.db_connector import DatabaseClient


class EventJobController:


	def main(self):
		conigDb = ConnectionSchema.from_dict(_ENV.db_default.__dict__)
		jobs = ParquetModel.get_active_jobs(conigDb)
		for job in jobs:
			params = None
			if job.isDynamicDate:
				if job.paramsDynamics is not None:
					query, params = QueryParamTransformer.transform(job.queryText, job.paramsDynamics, job.dbConnection.engine)
				elif job.isRangeDate is True:
					offsetDays = 0 if job.startHistory is None else job.startHistory
					startHistory = datetime.today() - timedelta(days=offsetDays)
					if job.historyDays is None:
						raise Exception(f'Job ID: {job.jobId} | Range without defined days')
					historyDays = startHistory - timedelta(days=job.historyDays)
					dynamicParams = {'startRange':startHistory.strftime("%Y-%m-%d"), 'endRange':historyDays.strftime("%Y-%m-%d")}
					query, params = QueryParamTransformer.transform(job.queryText, dynamicParams, job.dbConnection.engine)
				
				else:
					offsetDays = 0 if job.startHistory is None else job.startHistory
					startHistory = datetime.today() - timedelta(days=offsetDays)
					historyDays = startHistory - timedelta(days=job.historyDays - 1)
					for i in range((startHistory - historyDays).days + 1):
						dateParam = historyDays + timedelta(days=1)
						query, params = QueryParamTransformer.replace_params(job.queryText, dateParam, job.dbConnection.engine)

						
				
			if query.lower().startswith('select'):
				if len(params) > 0:
					result = DatabaseClient(job.dbConnection).select_all(query, params)
				else:
					result = DatabaseClient(job.dbConnection).select_all(query)
			else:
				if len(params) > 0:
					result = DatabaseClient(job.dbConnection).execute(query)

				result = DatabaseClient(job.dbConnection).execute(query)
			print(result)
			print(jobs)
			result = None


	def execute_query(self):
		DatabaseClient


		