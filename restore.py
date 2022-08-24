#!/usr/bin/python

from pysnmp.hlapi import *

class snmp(object):
	def __init__(self, host, community):
		self.host = host
		self.community = community
		
		self.commands = []
		
		self.ftp_server = {
			'ip':'',
			'ftp_user':'snmpro',
			'ftp_pass':'snmpro',
		}

		self.base_oid = '1.3.6.1.4.1.9.9.96.1.1.1.1'
		
		self.ccConfigCopyProtocol = '.2'
		self.ccConfigCopyProtocol_options = {
			'tftp':Integer(1),
			'ftp':Integer(2),
			'rcp':Integer(3),
			'scp':Integer(4),
			'sftp':Integer(5),
		}

		self.ccCopySourceFileType = '.3'
		self.ccCopySourceFileType_options = {
			'networkFile':Integer(1),
			'iosFile':Integer(2),
			'startupConfig':Integer(3),
			'runningConfig':Integer(4),
			'terminal':Integer(5),
		}

		self.ccCopyDestFileType = '.4'
		self.ccCopyDestFileType_options = {
			'networkFile':Integer(1),
			'iosFile':Integer(2),
			'startupConfig':Integer(3),
			'runningConfig':Integer(4),
			'terminal':Integer(5),
                }

		self.ccCopyServerAddress = '.5'
		#IpAddress()

		self.ccCopyFileName = '.6'
		#OctetString()

		self.ccCopyUserName = '.7'
		#OctetString()

		self.ccCopyUserPassword = '.8'
		#OctetString()

		self.ccCopyNotificationOnCompletion = '.9'
		#Integer()

		self.ccCopyState = '.10'
		self.ccCopyState_options = {
			'waiting':Integer(1),
			'running':Integer(2),
			'successful':Integer(3),
			'failed':Integer(4),
		}

		self.ccCopyTimeStarted = '.11'
		#TimeStamp()

		self.ccCopyTimeCompleted = '.12'
		#TimeStamp()

		self.ccCopyFailCause = '.13'
		self.ccCopyFailCause_options = {
			'unknown':Integer(1),
			'badFileName':Integer(2),
			'timeout':Integer(3),
			'noMem':Integer(4),
			'noConfig':Integer(5),
			'unsupportedProtocol':Integer(6),
			'someConfigApplyFailed':Integer(7),
		}

		self.ccCopyEntryRowStatus = '.14'
		self.ccCopyEntryRowStatus_options = {
			'active':Integer(1),
			'notInService':Integer(2),
			'createAndGo':Integer(4),
			'createAndWait':Integer(5),
			'destroy':Integer(6),
		}

		self.arbitrary_number = '.123'
		return

	def source_ftp(self):
		self.commands += [
			(self.base_oid + self.ccConfigCopyProtocol + self.arbitrary_number, self.ccConfigCopyProtocol_options['ftp']),
			(self.base_oid + self.ccCopySourceFileType + self.arbitrary_number, self.ccCopySourceFileType_options['networkFile']),
		]
		return
    
	def source_run(self):
		self.commands += [
			(self.base_oid + self.ccConfigCopyProtocol + self.arbitrary_number, self.ccConfigCopyProtocol_options['ftp']),
			(self.base_oid + self.ccCopySourceFileType + self.arbitrary_number, self.ccCopySourceFileType_options['runningConfig']),
		]
		return
    
	def source_start(self):
		self.commands += [
			(self.base_oid + self.ccConfigCopyProtocol + self.arbitrary_number, self.ccConfigCopyProtocol_options['ftp']),
			(self.base_oid + self.ccCopySourceFileType + self.arbitrary_number, self.ccCopySourceFileType_options['startupConfig']),
		]
		return

	def dest_ftp(self):
		self.commands += [
			(self.base_oid + self.ccCopyDestFileType + self.arbitrary_number, self.ccCopyDestFileType_options['networkFile']),
			(self.base_oid + self.ccCopyServerAddress + self.arbitrary_number, IpAddress(self.ftp_server['ip'])),
			(self.base_oid + self.ccCopyFileName + self.arbitrary_number, OctetString('{0}.txt'.format(self.host))),
			(self.base_oid + self.ccCopyUserName + self.arbitrary_number, OctetString(self.ftp_server['ftp_user'])),
			(self.base_oid + self.ccCopyUserPassword + self.arbitrary_number, OctetString(self.ftp_server['ftp_pass'])),
		]
		return
    
	def dest_run(self):
		self.commands += [
			(self.base_oid + self.ccCopyDestFileType + self.arbitrary_number, self.ccCopyDestFileType_options['runningConfig']),
			(self.base_oid + self.ccCopyServerAddress + self.arbitrary_number, IpAddress(self.ftp_server['ip'])),
			(self.base_oid + self.ccCopyFileName + self.arbitrary_number, OctetString('{0}.txt'.format(self.host))),
			(self.base_oid + self.ccCopyUserName + self.arbitrary_number, OctetString(self.ftp_server['ftp_user'])),
			(self.base_oid + self.ccCopyUserPassword + self.arbitrary_number, OctetString(self.ftp_server['ftp_pass'])),
		]
		return
    
	def dest_start(self):
		self.commands += [
			(self.base_oid + self.ccCopyDestFileType + self.arbitrary_number, self.ccCopyDestFileType_options['startupConfig']),
			(self.base_oid + self.ccCopyServerAddress + self.arbitrary_number, IpAddress(self.ftp_server['ip'])),
			(self.base_oid + self.ccCopyFileName + self.arbitrary_number, OctetString('{0}.txt'.format(self.host))),
			(self.base_oid + self.ccCopyUserName + self.arbitrary_number, OctetString(self.ftp_server['ftp_user'])),
			(self.base_oid + self.ccCopyUserPassword + self.arbitrary_number, OctetString(self.ftp_server['ftp_pass'])),
		]
		return

	def send(self):
		self.commands += [
			(self.base_oid + self.ccCopyEntryRowStatus + self.arbitrary_number, self.ccCopyEntryRowStatus_options['active']),
		]
		print 'sending commands!'
		for x in self.commands:
			s = setCmd(SnmpEngine(),
				CommunityData(self.community),
				UdpTransportTarget((self.host, 161)),
				ContextData(),
				x
			)
			s.next()
		# wait for completion
		while True:
			if self.status() == 3 or self.status() == 4:
				self.clear()
				break
		return

	def status(self):
		stat = getCmd(SnmpEngine(),
			CommunityData(self.community),
			UdpTransportTarget((self.host, 161)),
			ContextData(),
			(self.base_oid + self.ccCopyState + self.arbitrary_number, self.ccCopyState_options['running']),
			#('1.3.6.1.4.1.9.9.96.1.1.1.1.10.123',  Integer(2)),
		)
		status = stat.next()
		return status[3][0][1]
	
	def clear(self):
		s = setCmd(SnmpEngine(),
			CommunityData(self.community),
			UdpTransportTarget((self.host, 161)),
			ContextData(),
			(self.base_oid + self.ccCopyEntryRowStatus + self.arbitrary_number, self.ccCopyEntryRowStatus_options['destroy']),
			#('1.3.6.1.4.1.9.9.96.1.1.1.1.14.123',  Integer(6)),
		)
		s.next()
		return

if __name__ == '__main__':
	import sys
	if len(sys.argv) == 4:
		action = sys.argv[1]
		host = sys.argv[2]
		community = sys.argv[3]
		if community == 'rw':
			s = snmp(host, 'snmprw')
		elif community == 'ro':
			s = snmp(host, 'snmpro')
		if action == '--restore':
			print 'starting loop 1'
			s.clear()
			s.source_start()
			s.dest_ftp()
			s.send()
			print 'done'
			print 'starting loop 2'
			s.clear()
			s.source_ftp()
			s.dest_run()
			s.send()
			print 'done'
		elif action == '--runget':
			s.clear()
			s.source_run()
			s.dest_ftp()
			s.send()
		elif action == '--runset':
			s.clear()
			s.source_ftp()
			s.dest_run()
			s.send()
		elif action == '--startget':
			s.clear()
			s.source_start()
			s.dest_ftp()
			s.send()
		elif action == '--startset':
			s.clear()
			s.source_ftp()
			s.dest_start()
			s.send()
		# extra, just in case
		s.clear()
		print 'done'
	else:
		print 'Usage: {0} <action> <host> [rw/ro]'.format(sys.argv[0])
		print 'Actions :'
		print '\t--runget\tretrieve running configuration from device'
		print '\t--runset\tpushes FTP file to running configuration'
		print '\t--restore\trestores startup configuration into running configuration'
		print '\t--startget\tretrieve startup configuration from device'
		print '\t--startset\tpushes FTP file to startup configuration'
		exit(1)
