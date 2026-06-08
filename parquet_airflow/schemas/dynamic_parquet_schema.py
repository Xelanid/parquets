from typing import Any
from dataclasses import dataclass


@dataclass
class DynamicJobSchema:
	runId        : str
	jobId        : str
	params       : str
	outputPath   : str
	status       : str
	scheduledAt  : str
	startedAt    : str
	finishedAt   : str
	errorMessage : str

	@staticmethod
	def from_dict(obj:Any)->'DynamicJobSchema':
		assert isinstance(obj,dict)
		runId        = obj.get("run_id")
		jobId        = obj.get("job_id")
		params       = obj.get("params")
		outputPath   = obj.get("output_path")
		status       = obj.get("status")
		scheduledAt  = obj.get("scheduled_at")
		startedAt    = obj.get("started_at")
		finishedAt   = obj.get("finished_at")
		errorMessage = obj.get("error_message")
		return DynamicJobSchema(runId, jobId, params, outputPath, status, scheduledAt, startedAt, finishedAt, errorMessage)