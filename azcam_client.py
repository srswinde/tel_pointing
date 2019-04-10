from scottSock import scottSock
import time

AZCAM_IP = "10.130.133.138" #steward azcam testbed
#AZCAM_IP = "10.130.1.11"
AZCAM_PORT = 2402

import sys
cmds = [ 
		#"Reset()",
		"Set RemoteImageServerHost 10.130.132.183",
		"Set RemoteImageServerPort 1234",
		"Set RemoteImageFileName im10.fits",
		"Set RemoteImageServer 1", 
		"Set Globals.newroi 1",
		"Set Readoutmode Wait",
		"StartExposure 5.0 'object'"]
	

for cmd in cmds:
	s=scottSock( AZCAM_IP, AZCAM_PORT )
	print "{0} ".format(cmd),
	print s.converse("{0}\r\n".format(cmd))
	s.close()


#time.sleep(5)


#s=scottSock( AZCAM_IP, AZCAM_PORT )
#print s.converse( "{0}\r\n".format("readexposure") )
