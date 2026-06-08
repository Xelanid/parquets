
class JobsController:
	__slots__ = ('__job')
    
	def __init__(self, job: dict):
		self.__job = job
	
	def run(self):
		query = self.__job.get('query')
		print(query)