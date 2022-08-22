# SNMP Restoration Script

Sends SNMP read-write commands to a host that triggers an FTP upload of the startup-configuration to ftp://your-server

After the configuration is fully uploaded, the device triggers an FTP download of the startup-configuration into its own running-configuration.
