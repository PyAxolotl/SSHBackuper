from fabric.api import env, run, get, put
from getpass import getpass
from pathlib import Path
from uuid import uuid4

import shutil
import os

class BackupperException(object):
	"""docstring for BackupperException"""
	def __init__(self, *args, **kwargs):
		super(BackupperException, self).__init__(*args, **kwargs)
		
try:
	from .transport import *
except:
	from transport import *

class Backupper(object):
	pass
		

class CopyBackupper(Backupper):
	"""docstring for CopyBackupper"""
	def __init__(self, source, target, remove_on_backup=False):
		super(CopyBackupper, self).__init__()
		self.source = source 
		self.target = target
		self.remove_on_backup = remove_on_backup
		self.temp_dir = None
		self.initialize()

	def initialize(self):
		local_source = not self.source.isdistant(); local_target = not self.target.isdistant()
		if not local_source and not local_target:
			raise BackupperException(f"Source and Target can't be both on distant machines for backupper CopyBackupper")
		if local_source and not(os.path.isdir(self.source.path) or os.path.isfile(self.source.path)):
			raise BackupperException(f"Local source path: '{self.source.path}' does not exist")
		if local_source and local_target:
			self.target_type = "file" if (os.path.isfile(self.source.path) and not os.path.isdir(self.target.path)) else "dir"
			self.tranport = LocalToLocal(self,self.source,self.target)
		else:
			self.tranport = DistantToLocal(self,self.source,self.target) if local_target else LocalToDistant(self,self.source,self.target)
		if not local_source and self.source.password is None:
			self.source.password = getpass("password to the source machine:")
		if not local_target and self.target.password is None:
			self.target.password = getpass("password to the target machine:")

	def initdistantload(self):
		if self.temp_dir is None:
			self.temp_dir = str(uuid4()).replace('-','')
			os.mkdir(self.temp_dir); base = self.temp_dir
			env.host_string = self.source.host
			env.user = self.source.username
			env.password = self.source.password
		return self.temp_dir

	def localLoad(self,path):
		if os.path.isdir(path):
			for file in os.listdir(path):
				yield os.path.join(path,file)
		elif os.path.isfile(path):
			yield path
		else:
			raise BackupperException(f"Cannot load objet at path {path}")

	def localunload(self,from_,to_):
		if self.target_type == "dir":
			if not os.path.isdir(to_):
				os.mkdir(to_)
			if os.path.isfile(from_):
				shutil.copy(from_,os.path.join(to_,Path(from_).name))
			elif os.path.isdir(from_):
				shutil.copytree(from_,os.path.join(to_,Path(from_).name))
			else:
				raise BackupperException(f"Cannot copy objet at path {from_}")
		else:
			shutil.copy(from_,to_)

	def distantLoad(self,path,base=None):
		define_ = False
		if base is None:
			base = self.initdistantload();define_ = True

		cmd = f"test -d {path} && echo 1 || echo 2;"; 
		isdir = (int(run(cmd)) == 1)
		if define_:
			self.target_type = "file" if not isdir and not os.path.isdir(self.target.path) else "dir"

		if not isdir:
			target = os.path.join(base,Path(path).name)
			get(path,target)
			yield target
		else:
			content = [line.split() for line in run(f"ls -l {path}").split('\n')[1:]]
			nbase = os.path.join(base,Path(path).name)
			os.mkdir(nbase)
			for file in content:
				directory = (file[0][0] == "d")
				target = os.path.join(nbase,file[-1])
				if not directory:
					get('/'.join([path,file[-1]]),target)
					yield target
				else:
					for file in self.distantLoad('/'.join([path,file[-1]]),base=nbase):
						yield file

	def start(self):
		self.tranport.start()