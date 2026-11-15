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


import socket
import getpass
import stat
import paramiko
import posixpath
#from paramiko.py3compat import input


#>>> import paramiko
#>>> client = paramiko.SSHClient()
#>>> client.load_system_host_keys()
#>>> client.connect("d0gbert-devbox.local", username="d0gbert")
#>>> sftpcli = client.open_sftp()
#>>> sftpcli.listdir()

#>>> policy = paramiko.WarningPolicy()
#>>> client = paramiko.SSHClient()
#>>> client.set_missing_host_key_policy(policy)


#import paramiko
#k = paramiko.RSAKey.from_private_key_file("/Users/whatever/Downloads/mykey.pem")
#c = paramiko.SSHClient()
#c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#print "connecting"
#c.connect( hostname = "www.acme.com", username = "ubuntu", pkey = k )
#print "connected"
#commands = [ "/home/ubuntu/firstscript.sh", "/home/ubuntu/secondscript.sh" ]
#for command in commands:
#	print "Executing {}".format( command )
#	stdin , stdout, stderr = c.exec_command(command)
#	print stdout.read()
#	print( "Errors")
#	print stderr.read()
#c.close()



class sftp_interface:

   def __init__(self):
      self.config_values = {'port': 22,'authentication':'password'}
      self.sftp_conn = None
      pass

   def prepare(self, config_params = {}):
      self.config_values.update(config_params)


   def connect(self):
      the_username = self.config_values['username']
      policy = paramiko.WarningPolicy()
      hostname = socket.gethostbyname(self.config_values['hostname'])  #socket.getfqdn()
      client = paramiko.SSHClient()
      if self.config_values['authentication'] == 'public_key':   #Perform key authentication
         client.load_system_host_keys()
         client.connect(self.config_values['hostname'], username = the_username)
      else:
         client.set_missing_host_key_policy(policy)
         the_password = getpass.getpass('Connecting to %s@%s.  Enter Password: ' % (self.config_values['username'], self.config_values['hostname']))
         client.connect(self.config_values['hostname'], username = self.config_values['username'], password = the_password)
      self.sftp_conn = client.open_sftp()


   def disconnect(self):
      self.sftp_conn.close()

   def type(self):
      return 'remote'

   def does_url_exist(self,file_name):
      flag = True
      try:
         file_stat_attr = self.sftp_conn.stat(file_name)
      except:
         flag = False
      return flag
      #return os.path.exists(file_name)
   
   def abspath(self,file_url):
      return file_url
   
   def list_directory(self,file_url):
      return self.sftp_conn.listdir(file_url)
   
   def join_url(self,base_url,operand):
      return (base_url + '/' + operand)
   
   def is_file_url(self,file_url):
      file_stat_attr = self.sftp_conn.stat(file_url)
      kind = stat.S_IFMT(file_stat_attr.st_mode)
      if kind == stat.S_IFREG:
         return True
      else:
         return False
      #return os.path.isfile(file_url)
   
   def is_dir_url(self,file_url):
      file_stat_attr = self.sftp_conn.stat(file_url)
      kind = stat.S_IFMT(file_stat_attr.st_mode)
      if kind == stat.S_IFDIR:
         return True
      else:
         return False
   
   def put_file(self,from_url,to_url):  #
      self.sftp_conn.put(from_url, to_url)
      
   def get_file(self,from_url,to_url):
      self.sftp_conn.get(from_url, to_url)
      
   def remove_directory(self,file_url):
      self.sftp_conn.rmdir(file_url)
      
   def remove_file(self,file_url):
      self.sftp_conn.remove(file_url)

#Handles creating parent directories as well      
   def create_directory(self,file_url):
      try:
         self.sftp_conn.mkdir(file_url)
      except IOError:
         parent_path = posixpath.dirname(file_url)
         self.create_directory(parent_path)
         self.sftp_conn.mkdir(file_url)

   def set_file_dates(self,file_url,access_date,modified_date):
      date_tuple = (access_date,modified_date)
      self.sftp_conn.utime(file_url,date_tuple)

   def get_modified_date(self,file_url):
      file_stat_attr = self.sftp_conn.stat(file_url)
      return int(file_stat_attr.st_mtime)
      #for stat_name in file_stat_attr.keys():
      #   print stat_name, ": ", file_stat_attr[stat_name]
      #return file_stat_attr['st_mtime']

   def get_access_date(self,file_url):
      file_stat_attr = self.sftp_conn.stat(file_url)
      return int(file_stat_attr.st_atime)

def main():
   sftp_inst = sftp_interface()
   sftp_inst.prepare({'hostname': 'd0gbert-devbox.local', 'username': 'd0gbert', 'authentication': 'public_key'})
   sftp_inst.connect()
   curr_dir = '.'
   print("Listing Directory: %s" % (curr_dir,))
   print(sftp_inst.list_directory(curr_dir))
   curr_dir = sftp_inst.join_url(curr_dir,'hello.txt')
   print("Listing Directory: %s" % (curr_dir,))
   print(sftp_inst.list_directory(curr_dir))
#   print(sftp_inst.does_url_exist(sftp_inst.join_url(curr_dir,'test.c')))
#   print(sftp_inst.does_url_exist(sftp_inst.join_url(curr_dir,'dude')))   
#   print(sftp_inst.is_dir_url(sftp_inst.join_url(curr_dir,'svn')))
#   print(sftp_inst.is_file_url(sftp_inst.join_url(curr_dir,'svn')))
#   print(sftp_inst.get_modified_date(sftp_inst.join_url(curr_dir,'test.asm')))
   
   sftp_inst.disconnect()

   
if __name__ == '__main__':
   main()
