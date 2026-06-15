import pyarrow as pa
import pyarrow.parquet as pq

class JobsController:
	__slots__ = ('__job',)
    
	def __init__(self, job: dict):
		self.__job = job
	
	def run(self):
		query = self.__job.get('query')
		print(query)
	
	def test_pyarrow(self):
		data = {
			'id': [10],
			'provider_id': [3],
			'is_afilied': [True],
			'email': ['Joe.Doh@gmail.com']
		}

		table = pa.Table.from_pydict(data)
		pq.write_table(table, 'parquet_test.parquet')