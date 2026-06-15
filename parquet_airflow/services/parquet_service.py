import pyarrow as pa
import pyarrow.parquet as pq
from typing import Any
from parquet_airflow import _ENV

class ParquetService:
	__slots__ = ('__filepath',)

	def __init__(self):
		self.__filepath = _ENV['paths']['parquets']

	def run(self, data: list[dict[str, Any]] | dict[str, Any], filename: str):
		dataNormalized = self.__normalize_data(data)
		dataTable = pa.Table.from_pylist(dataNormalized)

		filepath = self.__filepath + filename
		pq.write_table(dataTable, filepath)

	def __normalize_data(self, data: list[dict[str, Any]] | dict[str, Any]) -> list[dict[str, Any]]:
		if isinstance(data, dict):
			data = [data]
		return data