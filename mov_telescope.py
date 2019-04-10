import socket
import struct
from itertools import product
from astro.locales import kittpeak, mtgraham, tucson, mtlemmon
from astro.angles import RA_angle, Deg10, Dec_angle, Hour_angle
import random
import numpy as np

VATT_CMD_STATUS_ALTAZ		=       0x0a10
VATT_CMD_STATUS_ALTABS		=       0x0a11
VATT_CMD_STATUS_TIMES		=       0x0a12
VATT_CMD_STATUS_SECONDARY1	=       0x0a13
VATT_CMD_STATUS_SECONDARY2	=       0x0a14
VATT_CMD_STATUS_TEMPS		=       0x0a15
VATT_CMD_STATUS_RELAY		=       0x0a16
VATT_CMD_STATUS_CUROBJ		=       0x0a20
VATT_CMD_MOVE_RADEC_REL_ALL =       0x0570

VATT_CMD_MOVE_ERROR_OOL      =  (0x0100)
VATT_CMD_MOVE_ERROR_QLCKD    =  (0x0200)
VATT_CMD_MOVE_ERROR_DRVDSBLD =  (0x0300)
VATT_CMD_MOVE_ERROR_NOTRCK   =  (0x0400)



DEG2CMDPAR = 3600000.0


class vattbin:

    def __init__(self):
        self.socket = None
        self.open_socket()

    def open_socket( self ):

        print("opening socket")
        self.socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.socket.settimeout(0.25)

        try:
            self.socket.connect( ("10.0.1.10", 1040) )
            retn = True
        except Exception as err:
            print ( "Could not connect to vatttel" )
            self.socket = None
            retn = False
        return False


    def sendrecv( self, cmd, *param_list ):

        cmd = self.pack_cmd(  cmd, *param_list)
        try:

            self.socket.sendall( cmd )
            resp = self.socket.recv( 64 )

        except IOError as err:

            if err.errno == 104: # connection reset by peer
                print( "connection reset by peer" )
                self.socket = None
                resp = None
            else:
                raise

        if resp is not None:
            return self.unpack_resp( resp )

        else:
            return resp


    def pack_cmd_old( self, command ):
        return ("VATT\x00".encode() +
                struct.pack('b', ( command >> 16) & 0xFF) +
                struct.pack('b', (command >> 8) & 0xFF ) +
                struct.pack( 'b', command & 0xFF ) )

    def pack_cmd(self, command, *param_list):
        return "VATT".encode() + struct.pack("!i"+len(param_list)*"i", command, *param_list )


    def unpack_resp( self, pkt ):
        """The response from the mnelson server is 64 network order bytes of
        unsigned short integers in micro arcseconds (1/3600000.0). """
        vals = [ val for val in struct.unpack('!16i', pkt) ]

        #the first two bytes are the header "VATT"
        return vals[2:]


    def goto( self, ra_deg, dec_deg ):
        ra = int(ra_deg*DEG2CMDPAR)
        dec = int(dec_deg*DEG2CMDPAR)
        resp = self.sendrecv(VATT_CMD_MOVE_RADEC_REL_ALL, ra, dec )
        return resp



def altaz_grid(
    start_alt=20,
    stop_alt=75,
    step_alt=10,
    start_az=0,
    stop_az=360,
    step_az=30,
    dither=False):
    dithers = [Deg10(-1), Deg10(1)]
    n_azs = [40, 25, 15, 10, 5, 4 ]
    ii = 0
    jj = 0
    coords = np.zeros((sum(n_azs, 2)))
    for alt in np.linspace(start_alt, stop_alt, 6):
        for az in np.linspace(start_az, stop_az, n_azs[ii]):
            coords[jj,:] = np.array([alt, az])
            jj+=1
        ii+=1

    return coords

if __name__ == "__main__":
    grid = altaz_grid()
    for (alt, az) in grid:
        print (alt, az)


