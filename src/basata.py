"""
    This file is part of the Basata backup software.

    Basata is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Basata is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Basata.  If not, see <http://www.gnu.org/licenses/>.

Copyright 2018 by Michael Burns
    
"""



import string
import os
import copy
import configparser
import shutil
import optparse
from basata_sftp_interface import sftp_interface

#sudo apt-get install cifs-utils
#sudo mount -t cifs -o username=d0gbert,password=PASSWORD //d0gbert-server/diskshare1 /mnt/shares/diskshare1


SAMPLE_CONFIG_SCRIPT = """
[DevBox_SVN]
interface = sftp_interface
hostname = d0gbert-devbox.local
username = d0gbert
authentication = public_key
port = 22
source_folder = ~/programming/basata_svn
destin_folder = /mnt/datadisk1/share1/programming/basata_svn
items: ${source_folder}/notes => ${destin_folder}/notes
       ${source_folder}/basata => ${destin_folder}/basata
selection = recent only
copy_mode = replace

[Windows_Example]
interface = sftp_interface
hostname = d0gbert-devbox.local
username = d0gbert
port = 22
items: C:\\Users\\d0gbert\\Documents\\programming\\dev_system => ./programming/basata_svn
       C:\\Users\\d0gbert\\Music\\iTunes\\iTunes Media\\Podcasts => ./Podcasts
selection = recent only
copy_mode = replace

[File_Repo]
source1_folder = ~
source2_folder = /mnt/sharedisk1/share1
destin_folder = /media/usbdisks/datadisk1/share1
items: ${source2_folder}/Documents => ${destin_folder}/Documents/
       ${source1_folder}/Videos/Music_Videos => ${destin_folder}/Media/Videos/Music_Videos
       ${source2_folder}/Pictures => ${destin_folder}/Media/Pictures
#       ${source2_folder}/wikipedia => ${destin_folder}/backups/wikipedia
       ${source2_folder}/kiwix_zim_files => ${destin_folder}/Media/ZIM_Files
selection = recent only
copy_mode = replace

[GLOBAL SETTINGS]
batch_mode = sequential
debug_level = 2

"""



#***  Loading config file: /Users/d0gbert/Documents/programming/dev_box/basata/basata_config.cfg
#Traceback (most recent call last):
#  File "basata.py", line 553, in <module>
#    main_program()
#  File "basata.py", line 522, in main_program
#    theapp.perform_all_restores()
#  File "basata.py", line 212, in perform_all_restores
#    self.perform_restore(backup_name)         
#  File "basata.py", line 233, in perform_restore
#    restore_inst = restore_unit(backup_name,self.backup_list[backup_name],self.debug_level)
#  File "basata.py", line 261, in __init__
#    self.dest_intf = self.load_interface(self.backup_params['destin_interface'])
#  File "basata.py", line 268, in load_interface
#    intf_inst.connect()
#  File "/Users/d0gbert/Documents/programming/dev_box/basata/basata_sftp_interface.py", line 68, in connect
#    t = paramiko.Transport((self.config_values['hostname'],self.config_values['port']))
#  File "/Library/Python/2.7/site-packages/paramiko/transport.py", line 325, in __init__
#    retry_on_signal(lambda: sock.connect((hostname, port)))
#  File "/Library/Python/2.7/site-packages/paramiko/util.py", line 279, in retry_on_signal
#    return function()
#  File "/Library/Python/2.7/site-packages/paramiko/transport.py", line 325, in <lambda>
#    retry_on_signal(lambda: sock.connect((hostname, port)))
#  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/socket.py", line 228, in meth
#    return getattr(self._sock,name)(*args)
#TypeError: an integer is required



class localfs_interface:

	def __init__(self):
		pass

	def prepare(self, config_params = {}):
		pass
		
	def connect(self):
		pass


	def generate_key_files(self):
		pass
		
	def disconnect(self):
		pass

	def type(self):
		return 'local'

	def does_url_exist(self,file_name):
		return os.path.exists(file_name)
		
	def abspath(self,file_url):
		#print "Abs path before: ", file_url
		dude = os.path.abspath(os.path.expanduser(file_url))
		#print "Abs path after:  ", dude
		return dude
	
	def list_directory(self,file_url):
		return os.listdir(file_url)
	
	def join_url(self,base_url,operand):
		return os.path.join(base_url,operand)
	
	def is_file_url(self,file_url):
		return os.path.isfile(file_url)
	
	def is_dir_url(self,file_url):
		return os.path.isdir(file_url)
	
	def put_file(self,from_url,to_url):  #
		#shutil.copyfile(from_url, to_url)
		shutil.copy(from_url,to_url)
		
	def get_file(self,from_url,to_url):
		pass
		
	def remove_directory(self,file_url):
		os.rmdir(file_url)
		
	def remove_file(self,file_url):
		os.remove(file_url)
		
	def create_directory(self,file_url):
		try:
			os.mkdir(file_url)
		except FileNotFoundError:
			existing_base = file_url
			folder_stack = []
			while not os.path.exists(existing_base):
				break_apart = os.path.split(existing_base)
				existing_base = break_apart[0]
				existing_base = break_apart[0]
				folder_stack.append(break_apart[1])
			while len(folder_stack) > 0:
				new_folder = folder_stack.pop()
				existing_base = os.path.join(existing_base, new_folder)
				os.mkdir(existing_base)


	def set_file_dates(self,file_url,access_date,modified_date):
		date_tuple = (access_date,modified_date)
		os.utime(file_url,date_tuple)

	def get_modified_date(self,file_url):
		return int(os.path.getmtime(file_url))

	def get_access_date(self,file_url):
		return int(os.path.getatime(file_url))

		
	def load_interface(self,interface_name):
		if interface_name not in BASATA_INTERFACES:
			return None
		intf_inst = BASATA_INTERFACES[interface_name]()
		intf_inst.prepare(self.backup_params[interface_name])



DEFAULT_GLOBAL_OPTIONS = {'batch_mode': 'sequential','debug_level': '10'}
DEFAULT_BACKUP_OPTIONS = {'items': {}, 'interface': 'localfs_interface', 'selection': 'recent only', 'copy_mode': 'replace'} 

BASATA_INTERFACES = {'localfs_interface': localfs_interface, 'sftp_interface': sftp_interface}


class basata_program:
	def __init__(self):
		pass
		self.global_settings = {'batch_mode': 'sequential'}
		self.backup_list = {}
		self.debug_level = 10
		
	def load_config(self,config_filename):
		#configparser.ConfigParser(defaults=None, dict_type=dict, allow_no_value=False, delimiters=('=', ':'), comment_prefixes=('#', ';'), inline_comment_prefixes=None, strict=True, empty_lines_in_values=True, default_section=configparser.DEFAULTSECT, interpolation=BasicInterpolation(), converters={})
		config= configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
		try:
			with open(config_filename, 'r') as cfgfile:
				config.read_file(cfgfile)
		except:
			print("Config File not found: %s" % (config_filename,))
			raise SystemExit(1)
		#config.read(config_filename)
		self.debug_message('Loading config file: %s' % (config_filename,),8)
		self.global_settings = DEFAULT_GLOBAL_OPTIONS
		for option_name in config.options('GLOBAL SETTINGS'):
			self.global_settings[option_name] = config.get('GLOBAL SETTINGS',option_name)
			#self.debug_message('Global option: %s= %s' % (option_name,config.get('GLOBAL SETTINGS',option_name)),10)
		self.debug_level = int(self.global_settings['debug_level'])
		for section_name in config.sections():
			if section_name == 'GLOBAL SETTINGS':
				break
			self.debug_message('Reading config section: %s' % (section_name,),10)
			self.backup_list[section_name] = copy.copy(DEFAULT_BACKUP_OPTIONS)
			for option_name in config.options(section_name):
				self.backup_list[section_name][option_name] = config.get(section_name,option_name)
			#Split apart sources
			#self.backup_list[section_name]['destination'] = os.path.abspath(os.path.expanduser(self.backup_list[section_name]['destination']))
			parse_items = {}
			for line_entry in self.backup_list[section_name]['items'].split("\n"):
				if line_entry.find("=>")>1:
					split_line = line_entry.split("=>")
					key_name = split_line[0].strip()
					the_value = split_line[1].strip()
					parse_items[key_name] = the_value
				else:
					parse_items[line_entry.strip()] = line_entry.strip()
			self.backup_list[section_name]['items'] = parse_items
			

	def perform_all_backups(self, mode='verify'):
		self.debug_message(self.backup_list,10)
		for backup_name in list(self.backup_list.keys()):
			self.perform_backup(backup_name, mode)
			
	def perform_all_cleanups(self, mode='verify'):
		self.debug_message(self.backup_list,10)
		for backup_name in list(self.backup_list.keys()):
			self.perform_cleanup(backup_name, mode)			

	def perform_all_purges(self, mode='verify'):
		self.debug_message(self.backup_list,10)
		for backup_name in list(self.backup_list.keys()):
			self.perform_purge(backup_name, mode)			

	def perform_all_restores(self, mode='verify'):
		self.debug_message(self.backup_list,10)
		for backup_name in list(self.backup_list.keys()):
			self.perform_restore(backup_name, mode)			
 
	def perform_backup(self,backup_name, mode='verify'):
		backup_inst = backup_unit(backup_name,self.backup_list[backup_name],mode,self.debug_level)
		self.debug_message('Performing Backup for %s in %s mode' % (backup_name,mode.upper()),1)
		backup_inst.start_backup()
		self.debug_message('Finished Backup for %s' % (backup_name,),1)
	
	def perform_cleanup(self,backup_name, mode='verify'):
		cleanup_inst = cleanup_unit(backup_name,self.backup_list[backup_name],mode,self.debug_level)
		self.debug_message('Performing Cleanup for %s in %s mode' % (backup_name,mode.upper()),1)
		cleanup_inst.start_cleanup()
		self.debug_message('Finished Cleanup for %s' % (backup_name,),1)		 

	def perform_purge(self,backup_name, mode='verify'):
		purge_inst = purge_unit(backup_name,self.backup_list[backup_name],mode,self.debug_level)
		self.debug_message('Performing Purge for %s in %s mode' % (backup_name,mode.upper()),1)
		purge_inst.start_purge()
		self.debug_message('Finished Purge for %s' % (backup_name,),1)		 

	def perform_restore(self,backup_name, mode='verify'):
		restore_inst = restore_unit(backup_name,self.backup_list[backup_name],mode,self.debug_level)
		self.debug_message('Performing Restore for %s in %s mode' % (backup_name,mode.upper()),1)
		restore_inst.start_restore() 
		self.debug_message('Finished Restore for %s' % (backup_name,),1)		
 
	def debug_message(self,message,level):
		if(level <= self.debug_level):
			print('*** ', message)




		
		
class basata_unit:
	def __init__(self, bkup_name, backup_settings = {}, mode='verify', debug_lvl = 2):
		self.backup_params = backup_settings
		self.backup_name = bkup_name
		self.debug_level = debug_lvl
		self.module_mode = mode
		self.srce_intf = self.load_interface('localfs_interface')
		self.dest_intf = self.load_interface(self.backup_params['interface'])
		
	def load_interface(self,interface_name):
		if interface_name not in BASATA_INTERFACES:
			return None 
		self.debug_message('Loading interface: %s' % (interface_name,),1)		
		intf_inst = BASATA_INTERFACES[interface_name]()
		intf_inst.prepare(self.backup_params)
		intf_inst.connect()
		return intf_inst
		
		
		#if interface_name == 'localfs_interface':
		#	return localfs_interface()
		#elif interface_name == 'sftp_interface':
		#	sftp_inst = sftp_interface()
		#	hostname = self.backup_params['hostname']
		#	username = self.backup_params['username']
		#	port = int(self.backup_params['port'])
		#	if self.backup_params.has_key('keyfile'):
		#		sftp_inst.connect_by_key(hostname,username,port,self.backup_params['keyfile'])
		#	else:
		#		sftp_inst.connect(hostname,username,port)
		#	return sftp_inst

	def is_source_newer(self, source_file, dest_file):
		source_ts = self.srce_intf.get_modified_date(source_file)
		dest_ts = self.dest_intf.get_modified_date(dest_file)
		if source_ts > dest_ts:
			return True
		else:
			return False	

	def is_dest_newer(self, source_file, dest_file):
		source_ts = self.srce_intf.get_modified_date(source_file)
		dest_ts = self.dest_intf.get_modified_date(dest_file)
		if dest_ts > source_ts:
			return True
		else:
			return False	

			
	def debug_message(self,message,level):
		if(level <= self.debug_level):
			print('*** ', message)



class backup_unit(basata_unit):

	def start_backup(self):
		self.debug_message('Performing Backup for %s' % (self.backup_name),2)
		for source_name in list(self.backup_params['items'].keys()):
			source_path = self.srce_intf.abspath(source_name)
			dest_path = self.dest_intf.abspath(self.backup_params['items'][source_name])
			self.debug_message('%s => %s' % (source_path, dest_path),2)
			if self.srce_intf.does_url_exist(source_path):
				if self.srce_intf.is_file_url(source_path):
					self.backup_file(source_path, dest_path, source_name) 
				else:
					if not self.dest_intf.does_url_exist(dest_path):
						if self.module_mode == 'change':
							self.dest_intf.create_directory(dest_path)
					self.debug_message('Backing up folder: %s' % (source_name,),3)
					self.backup_folder_contents(source_path, dest_path)
			else:
				self.debug_message('Source not found: %s' % (source_name,),1)


	def backup_folder_contents(self, source_folder_path, dest_folder_path):
		self.debug_message('Searching folder: %s' % (source_folder_path,),8)
		folder_contents = self.srce_intf.list_directory(source_folder_path)
		for dir_entry in folder_contents:
			if len(dir_entry)>0 and dir_entry[0]!='.':
				source_entry_path = self.srce_intf.join_url(source_folder_path,dir_entry)
				dest_entry_path = self.dest_intf.join_url(dest_folder_path,dir_entry)
				if self.srce_intf.is_dir_url(source_entry_path):
					if not self.dest_intf.does_url_exist(dest_entry_path):
						if self.module_mode == 'change':
							self.dest_intf.create_directory(dest_entry_path)
					self.backup_folder_contents(source_entry_path,dest_entry_path)
				elif self.srce_intf.is_file_url(source_entry_path):
					self.backup_file(source_entry_path, dest_entry_path, dir_entry) 
				else:
					pass

	def backup_file(self, source_path, dest_path, file_name):
		if not self.dest_intf.does_url_exist(dest_path):
			self.debug_message("Backing up file \"%s\" to %s" % (file_name,dest_path),2)
			self.copy_file(source_path, dest_path)
		elif self.backup_params['selection'] == 'all':
			self.debug_message("Overwriting file \"%s\" to %s" % (file_name,dest_path),2)
			self.copy_file(source_path, dest_path)
		elif self.backup_params['selection'] == 'recent only' and self.is_source_newer(source_path,dest_path): 
			self.debug_message("Committing file \"%s\" to %s" % (file_name,dest_path),2)
			self.copy_file(source_path, dest_path)
		else:
			self.debug_message("Skipping file \"%s\" located at %s" % (file_name,dest_path),5)
	
		
	def copy_file(self, source_path, dest_path):
		if self.module_mode == 'change' and self.backup_params['copy_mode'] == 'replace':
			access_ts = self.srce_intf.get_access_date(source_path)
			modified_ts = self.srce_intf.get_modified_date(source_path)
			if self.srce_intf.type() == 'local' and self.dest_intf.type() == 'local':
				self.srce_intf.put_file(source_path, dest_path)
			elif self.srce_intf.type() == 'remote' and self.dest_intf.type() == 'local':
				self.srce_intf.get_file(source_path, dest_path)
			elif self.srce_intf.type() == 'local' and self.dest_intf.type() == 'remote':
				self.dest_intf.put_file(source_path, dest_path)
			else:
				pass
			self.dest_intf.set_file_dates(dest_path,access_ts,modified_ts)
			#print "Copying %s to %s" % (source_path, dest_path)
		else:
			pass
		

	###############################

class restore_unit(basata_unit):

	def start_restore(self):
		self.debug_message('Performing Restore for %s' % (self.backup_name),2)
		for source_name in list(self.backup_params['items'].keys()):
			#source_path = self.backup_params['sources'][source_name]
			source_path = self.srce_intf.abspath(source_name)
			dest_path = self.dest_intf.abspath(self.backup_params['items'][source_name])
			self.debug_message('%s <= %s' % (source_path, dest_path),2)
			if self.dest_intf.does_url_exist(dest_path):
				if self.dest_intf.is_file_url(dest_path):
					self.restore_file(source_path, dest_path, dest_path)
				else:
					if not self.srce_intf.does_url_exist(source_path):
						if self.module_mode == 'change':
							self.srce_intf.create_directory(source_path)
					self.debug_message('Restoring folder: %s' % (source_name,),5)
					self.restore_folder_contents(dest_path, source_path)
			else:	
				self.debug_message('Destination not found: %s' % (dest_path,),1)


	def restore_folder_contents(self, dest_folder_path, source_folder_path): 
		self.debug_message('Searching folder: %s' % (source_folder_path,),8)
		folder_contents = self.dest_intf.list_directory(dest_folder_path)
		for dir_entry in folder_contents:
			if len(dir_entry)>0 and dir_entry[0]!='.':
				source_entry_path = self.srce_intf.join_url(source_folder_path,dir_entry)
				dest_entry_path = self.dest_intf.join_url(dest_folder_path,dir_entry)
				if self.dest_intf.is_dir_url(dest_entry_path):
					if not self.srce_intf.does_url_exist(source_entry_path):
						if self.module_mode == 'change':
							self.srce_intf.create_directory(source_entry_path)
						self.debug_message('Restoring folder from %s=%s=%s' % (dest_folder_path,dir_entry,dest_entry_path,),2)
					self.restore_folder_contents(dest_entry_path, source_entry_path)
				elif self.dest_intf.is_file_url(dest_entry_path):
					self.restore_file(source_entry_path, dest_entry_path, dir_entry)
				else:
					pass

	def restore_file(self, source_path, dest_path, file_name):
		if not self.srce_intf.does_url_exist(source_path):
			self.debug_message("Restoring file \"%s\" to %s" % (file_name,source_path),2)
			self.copy_file(source_path, dest_path)
		elif self.backup_params['selection'] == 'all':
			self.debug_message("Overwriting file \"%s\" to %s" % (file_name,source_path),2)
			self.copy_file(source_path, dest_path)
		elif self.backup_params['selection'] == 'recent only' and self.is_dest_newer(source_path,dest_path): 
			self.debug_message("Updating file \"%s\" to %s" % (file_name,source_path),2)
			self.copy_file(source_path, dest_path)
		else:
			self.debug_message("Skipping file \"%s\" located at %s" % (file_name,source_path),3)
	
		
	def copy_file(self, source_path, dest_path):
		if self.module_mode == 'change' and self.backup_params['copy_mode'] == 'replace':
			access_ts = self.dest_intf.get_access_date(dest_path)
			modified_ts = self.dest_intf.get_modified_date(dest_path)
			if self.srce_intf.type() == 'local' and self.dest_intf.type() == 'local':
				self.dest_intf.put_file(dest_path, source_path)
			elif self.srce_intf.type() == 'remote' and self.dest_intf.type() == 'local':
				self.srce_intf.put_file(dest_path, source_path)
			elif self.srce_intf.type() == 'local' and self.dest_intf.type() == 'remote':
				self.dest_intf.get_file(dest_path, source_path)
			else:
				pass 
			self.srce_intf.set_file_dates(source_path,access_ts,modified_ts)
			#print "Copying %s to %s" % (source_path, dest_path)
		else:
			pass


	###############################

class cleanup_unit(basata_unit):

	def start_cleanup(self):
		#dest_path = self.backup_params['destination']
		self.debug_message('Performing Removal for %s' % (self.backup_name,),2)
		for source_name in list(self.backup_params['items'].keys()):
			#source_path = self.backup_params['sources'][source_name]
			source_path = self.srce_intf.abspath(source_name)
			dest_path = self.dest_intf.abspath(self.backup_params['items'][source_name])
			#backup_dest_path = self.dest_intf.join_url(dest_path,source_name)
			self.debug_message('%s =* %s' % (source_path, dest_path),2)
			if self.dest_intf.is_file_url(dest_path):
				self.cleanup_file(dest_path, source_path)
			else:
				self.debug_message('Cleaning up folder: %s' % (source_name,),5)
				self.cleanup_folder_contents(dest_path, source_path)


	def cleanup_folder_contents(self, dest_folder_path, source_folder_path): 
		self.debug_message('Searching folder: %s' % (source_folder_path,),8)
		folder_contents = self.dest_intf.list_directory(dest_folder_path)
		for dir_entry in folder_contents:
			if len(dir_entry)>0 and dir_entry[0]!='.':
				source_entry_path = self.srce_intf.join_url(source_folder_path,dir_entry)
				dest_entry_path = self.dest_intf.join_url(dest_folder_path,dir_entry)
				if self.dest_intf.is_dir_url(dest_entry_path):
					self.cleanup_folder_contents(dest_entry_path, source_entry_path)
					if not self.srce_intf.does_url_exist(source_entry_path):
						if self.module_mode == 'change':
							self.dest_intf.remove_directory(dest_entry_path)
						self.debug_message('Removing folder from %s' % (dest_entry_path,),2)
				elif self.dest_intf.is_file_url(dest_entry_path):
					self.cleanup_file(dest_entry_path, source_entry_path)
				else:
					pass

	def cleanup_file(self, dest_path, source_path): 
		self.debug_message("Checking if source exists: %s" % (source_path,),5)
		if not self.srce_intf.does_url_exist(source_path):
			if self.module_mode == 'change':
				self.dest_intf.remove_file(dest_path) 
			self.debug_message('Removing file from %s' % (dest_path,),2)
		else:
			self.debug_message('File still at source %s' % (source_path,),3)
	 
	###############################

class purge_unit(basata_unit):

	def start_purge(self):
		#dest_path = self.backup_params['destination']
		self.debug_message('Performing Removal for %s' % (self.backup_name,),2)
		for source_name in list(self.backup_params['items'].keys()):
			#source_path = self.backup_params['sources'][source_name]
			source_path = self.srce_intf.abspath(source_name)
			dest_path = self.dest_intf.abspath(self.backup_params['items'][source_name])
			#backup_dest_path = self.dest_intf.join_url(dest_path,source_name)
			self.debug_message('%s =* %s' % (source_path, dest_path),2)
			if self.srce_intf.is_file_url(dest_path):
				self.purge_file(dest_path, source_path)
			else:
				self.debug_message('Checking folder for purge: %s' % (source_name,),5)
				self.purge_folder_contents(dest_path, source_path)


	def purge_folder_contents(self, dest_folder_path, source_folder_path): 
		self.debug_message('Searching folder: %s' % (dest_folder_path,),8)
		folder_contents = self.srce_intf.list_directory(source_folder_path)
		for dir_entry in folder_contents:
			if len(dir_entry)>0 and dir_entry[0]!='.':
				source_entry_path = self.srce_intf.join_url(source_folder_path,dir_entry)
				dest_entry_path = self.dest_intf.join_url(dest_folder_path,dir_entry)
				if self.srce_intf.is_dir_url(source_entry_path):
					self.purge_folder_contents(dest_entry_path, source_entry_path)
					if not self.dest_intf.does_url_exist(dest_entry_path):
						if self.module_mode == 'change':
							self.srce_intf.remove_directory(source_entry_path)
						self.debug_message('Removing folder from %s' % (source_entry_path,),2)
				elif self.srce_intf.is_file_url(source_entry_path):
					self.purge_file(dest_entry_path, source_entry_path)
				else:
					pass

	def purge_file(self, dest_path, source_path): 
		self.debug_message("Checking if destination exists: %s" % (dest_path,),5)
		if not self.dest_intf.does_url_exist(dest_path):
			if self.module_mode == 'change':
				self.srce_intf.remove_file(source_path) 
			self.debug_message('Removing file from %s' % (source_path,),2)
		else:
			self.debug_message('File still at source %s' % (dest_path,),3)




def main_program():
	argparse = optparse.OptionParser(description="Basata Backup Utility | Copyright 2018 by Michael Burns ",
												usage="usage: basata [options] (backup|restore|cleanup|purge|createcfg)",
												version="version 3.0")
	argparse.add_option("-m","--mode",dest="basata_mode",default="verify",help="Mode: (verify,change)")
	argparse.add_option("-c","--configfile",dest="configfilename",default=".basata.cfg",help="Location of config file")
	argparse.add_option("-b","--backupname",dest="backupname",default="all",help="Name of specific backup to run")	
	(options, args) = argparse.parse_args()
	if len(args) < 1:
		print("*** No command given for Backup Program")
		return

	configfilename = os.path.abspath(options.configfilename)
	#logfilename = os.path.abspath(options.logfilename)
	backupname = options.backupname
	basata_mode = options.basata_mode
	#errorfilename = os.path.abspath(options.errorfilename)
	
	theapp= basata_program()

	command = args[0]
	if command == "backup":
		theapp.load_config(configfilename)
		if backupname == 'all':
			theapp.perform_all_backups(mode=basata_mode)
		else:
			theapp.perform_backup(backupname, mode=basata_mode)
	elif command == "restore":
		theapp.load_config(configfilename)
		if backupname == 'all':
			theapp.perform_all_restores(mode=basata_mode)
		else:
			theapp.perform_restore(backupname, mode=basata_mode)
	elif command == "cleanup":
		theapp.load_config(configfilename)
		if backupname == 'all':
			theapp.perform_all_cleanups(mode=basata_mode)
		else:
			theapp.perform_cleanup(backupname, mode=basata_mode)
	elif command == "purge":
		theapp.load_config(configfilename)
		if backupname == 'all':
			theapp.perform_all_purges(mode=basata_mode)
		else:
			theapp.perform_purge(backupname, mode=basata_mode)
	elif command == "createcfg":
		cfgfile = open(configfilename,'w')
		cfgfile.write(SAMPLE_CONFIG_SCRIPT)
		cfgfile.close()
		print("Sample Config File created at: ", options.configfilename)
	else:
		print("*** Invalid command used with Backup Program")


if __name__ == "__main__":
	main_program()
