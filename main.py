try:
	from .backupper import *
except:
	from backupper import *
try:
	from .transport import *
except:
	from transport import *

import argparse
import sys


class Directory(object):
	"""docstring for Directory"""
	def __init__(self, path,host=None,port=None,username=None,password=None):
		super(Directory, self).__init__()
		self.path = path
		self.host = host
		self.port = port
		self.username = username
		self.password = password

	def isdistant(self):
		return self.host is not None and not self.host.startswith("127.0.0")
		
		

if __name__ == "__main__":

	PROGRAM_POSITIONNAL_ARGUMENTS = [
		{"name":'sdir', "type":str,"help":'Source directory'},
		{"name":'tdir', "type":str,"help":'Target directory'}
	]

	PROGRAM_OPTIONNAL_ARGUMENTS = {
		'--sip':{
			"type":str,"help":'Source ip address or domain name (local machine will picked as source if nothing is specified)',"dest":"source_address","default":None
		},'--su':{
			"dest":"source_user", "type":str,"help":'Username for the source machine',"default":None
		},'--sp':{
			"dest":"source_pass", "type":str,"help":'Password for the source machine',"default":None
		},'--sP':{
			"dest":"source_port", "type":str,"help":'SSH port for the source machine',"default":None
		},'--tip':{
			"type":str,"help":'Target ip address or domain name (local machine will picked as target if nothing is specified)',"dest":"target_address","default":None
		},'--tu':{
			"dest":"target_user", "type":str,"help":'Username for the target machine',"default":None
		},'--tp':{
			"dest":"target_pass", "type":str,"help":'Password for the target machine',"default":None
		},'--tP':{
			"dest":"target_port", "type":str,"help":'SSH port for the target machine',"default":None
		},'--verbose':{
			"":["-v"],"dest":"verbose", "action":'count',"help":'Verbose',"default":None
		},'--log':{
			"dest":"log_target", "type":str,"help":'Path for the logging directory/file.',"default":None
		},'--rm':{
			"const":True,"action":"store_const", "help":'Remove data from source after a successful backup',"default":False
		}
	}

	parser = argparse.ArgumentParser(
		prog='sshbackup',
		description='Python script that can be used to back up data from a directory located at a distant/local machine to another directory located at a distant/local machine using ssh and/or scp'
	)

	for arg in sorted(PROGRAM_POSITIONNAL_ARGUMENTS,key=lambda x:x['name']):
		parser.add_argument(arg.pop('name'), **arg)

	for arg in sorted(PROGRAM_OPTIONNAL_ARGUMENTS):
		aliases =  PROGRAM_OPTIONNAL_ARGUMENTS[arg].pop('',[])
		parser.add_argument(arg, *aliases, **PROGRAM_OPTIONNAL_ARGUMENTS[arg])

	args = parser.parse_args(sys.argv[1:])

	source = Directory(
		args.sdir,host=args.source_address,port=args.source_port,
		username=args.source_user,password=args.source_pass
	)

	target = Directory(
		args.tdir,host=args.target_address,port=args.target_port,
		username=args.target_user,password=args.target_pass
	)

	unzipped = CopyBackupper( source, target, remove_on_backup=args.rm ).start()


