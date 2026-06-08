import datetime
from typing import Any, Dict
from dataclasses import dataclass
from .connection_schema import ConnectionSchema

@dataclass
class ParquetJobSchema:
	jobId          : int
	jobName        : str
	dbName         : str
	connectionId   : int
	queryText      : str
	outputFile     : str
	cronJob        : datetime
	runOnceAt      : datetime
	isActive       : bool
	lastRunAt      : datetime
	nextRunAt      : datetime
	isDynamicDate  : bool
	paramsDynamics : Dict
	dbConnection   : ConnectionSchema
	createdAt      : str
	updatedAt      : str
	isRangeDate	   : bool
	startHistory   : int
	historyDays    : int



	@staticmethod
	def from_dict(obj:Any)->'ParquetJobSchema':
		assert isinstance(obj, dict)
		jobId          = obj.get("job_id")
		jobName        = obj.get("job_name")
		dbName         = obj.get("database_name")
		connectionId   = obj.get("connection_id")
		queryText      = obj.get("query_text")
		outputFile     = obj.get("output_file")
		cronJob        = obj.get("cron_job")
		runOnceAt      = obj.get("run_once_at")
		isActive       = obj.get("is_active")
		lastRunAt      = obj.get("last_run_at")
		nextRunAt      = obj.get("next_run_at")
		isDynamicDate  = obj.get("is_dynamic_date")
		paramsDynamics = obj.get("params_dynamics")
		dbConnection   = ConnectionSchema.from_dict(obj)
		createdAt      = obj.get("created_at")
		updatedAt      = obj.get("updated_at")
		return ParquetJobSchema(jobId, jobName, dbName, connectionId, queryText, outputFile, cronJob, runOnceAt, isActive, lastRunAt, nextRunAt, isDynamicDate, paramsDynamics, dbConnection, createdAt, updatedAt)
