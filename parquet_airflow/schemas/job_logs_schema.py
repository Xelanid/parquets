import datetime
from typing import Any
from dataclasses import dataclass

@dataclass
class JobLogSchema:
	logId    	 : int
	jobId    	 : int
	startTime	 : datetime
	endTime  	 : datetime
	status   	 : str
	errorMessage : str

	@staticmethod
	def from_dict(obj:Any)->'JobLogSchema':
		assert isinstance(obj, dict)
		logId        = obj.get("log_id")
		jobId        = obj.get("job_id")
		startTime    = obj.get("start_time")
		endTime      = obj.get("end_time")
		status       = obj.get("status")
		errorMessage = obj.get("error_message")
		return JobLogSchema(logId, jobId, startTime, endTime, status, errorMessage)