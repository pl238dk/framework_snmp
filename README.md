# Base SNMP Library

Connects via SNMP and has functions to pull basic interface data from the standard SNMP MIB.

```
>>> host = '192.168.1.1'
>>> s = snmp(host, community='snmpro')
>>> data = s.get_all_interface_info()
```

# SNMP Restoration Script

Sends SNMP read-write commands to a host that triggers an FTP upload of the startup-configuration to ftp://your-server

After the configuration is fully uploaded, the device triggers an FTP download of the startup-configuration into its own running-configuration.

## Authentication

Unfortunately, credentials would need to be hard-coded in the most recent version.

#### restore.py

For `restore.py` - FTP server authentication, under `__init__()`

```
    self.ftp_server = {
        'ip': '',
        'ftp_user': '',
        'ftp_pass': '',
    }
```

Each instantiation requires passing the SNMP community string (v2) :

```
>>> host = '192.168.1.1'
>>> community = 'snmpro'
>>> s = snmp(host, community)
```

#### snmp.py

Credentials are passed via object instantiation, but has a default of 'snmpro' if none are provided.

For 'snmpro' default using the base library :
```
>>> host = '192.168.1.1'
>>> s = snmp(host)
```

For specific community string using the base library :
```
>>> host = '192.168.1.1'
>>> community = 'snmprw'
>>> s = snmp(host, community=community)
