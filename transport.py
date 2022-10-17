from tqdm import tqdm

class Transport(object):
	def __init__(self, backupper, source, target):
		super(Transport, self).__init__()
		self.backupper = backupper
		self.source = source
		self.target = target
		

class LocalToLocal(Transport):
	"""docstring for LocalToLocal"""
	def __init__(self, *args,**kwargs):
		super(LocalToLocal, self).__init__(*args,**kwargs)

	def start(self):
		for file in tqdm(self.backupper.localLoad(self.source.path)):
			self.backupper.localunload(file,self.target.path)


class DistantToLocal(Transport):
	"""docstring for DistantToLocal"""
	def __init__(self, *args,**kwargs):
		super(DistantToLocal, self).__init__(*args,**kwargs)

	def start(self):
		for file in tqdm(self.backupper.distantLoad(self.source.path)):
			self.backupper.localunload(file,self.target.path)
