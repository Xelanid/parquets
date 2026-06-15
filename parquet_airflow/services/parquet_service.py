import pyarrow as pa
import pyarrow.parquet as pq
from typing import Any

class ParquetService:
	__slots__ = ('__filepath',)

	def __init__(self):
		self.__filepath = 'storage/parquets'

	def run(self, data: list[dict[str, Any]] | dict[str, Any], filename: str):
		if isinstance(data, dict):
			data = [data]
		dataTable = pa.Table.from_pylist(data)

		filepath = self.__filepath + filename
		pq.write_table(dataTable, filepath)