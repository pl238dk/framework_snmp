#
# SNMP Read
#

from pysnmp.hlapi import *

class snmp(object):
	def __init__(self, host, community=None):
		standard_ro = 'snmpro'
		self.community = community if community is not None else standard_ro
		self.host = host
		return
	
	def get(self, oid):
		output = getCmd(
			SnmpEngine(),
			CommunityData(self.community),
			UdpTransportTarget((self.host, 161)),
			ContextData(),
			ObjectType(ObjectIdentity(oid)),
		)
		errorIndication,errorStatus,errorIndex,varBinds = next(output)
		return varBinds
	
	def bulk(self, count, oid_list):
		bulk_output = bulkCmd(
			SnmpEngine(),
			CommunityData(self.community),
			UdpTransportTarget((self.host, 161)),
			ContextData(),
			0,
			count,
			*oid_list,
		)
		output = [next(bulk_output) for _ in range(count)]
		return output
	
	def get_interface_count(self):
		oid_ifNumber = '1.3.6.1.2.1.2.1.0'
		output_raw = self.get(oid_ifNumber)
		oid_raw,val_raw = output_raw[0]
		output = val_raw._value
		return output
	
	def get_all_interface_info(self, oid_list=None):
		# TODO : make <list 'oid_list'> operational
		'''
			2	ifDescr
			3	ifType
			4	ifMtu
			5	ifSpeed
			6	ifPhysAddress
			7	ifAdminStatus
			8	ifOperStatus
			9	ifLastChange
			10	ifInOctets
			11	ifInUcastPkts
			12	ifInNUcastPkts
			13	ifInDiscards
			14	ifInErrors
			15	ifInUnknownProtos
			16	ifOutOctets
			17	ifOutUcastPkts
			18	ifOutNUcastPkts
			19	ifOutDiscards
			20	ifOutErrors
			21	ifOutQLen
			22	ifSpecific
		'''
		oid_ifDescr = '1.3.6.1.2.1.2.2.1.2'
		oid_ifPhysAddress = '1.3.6.1.2.1.2.2.1.6'
		
		ifNumber = self.get_interface_count()
		
		bulk_output = self.bulk(
			ifNumber,
			[
				ObjectType(ObjectIdentity(oid_ifDescr)),
				ObjectType(ObjectIdentity(oid_ifPhysAddress)),
			]
		)
		bulk_varBinds = [
			varBinds
			for
			errorIndication,errorStatus,errorIndex,varBinds
			in bulk_output
		]
		# below output does not check for duplicate interface names
		output = {
			desc_raw[1].__str__()
			:
			':'.join([f'{x:X}' for x in mac_raw[1]])
			for
			(desc_raw, mac_raw)
			in bulk_varBinds
		}
		return output

if __name__ == '__main__':
	host = ''
	s = snmp(host)
	result = s.get_all_interface_info()