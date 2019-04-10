


import binascii
import socket
import struct
import sys

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float, SmallInteger, Text, BOOLEAN
from sqlalchemy import TIMESTAMP as DATETIME
from socket import timeout
from socket import timeout
import select
import socket
from .baseclasses import logger, config, getter
import errno
import datetime
import pandas as pd
import errno
from collections import OrderedDict

Base = declarative_base()

VATT_CMD_STATUS_ALTAZ		=       0x0a10
VATT_CMD_STATUS_ALTABS		=       0x0a11
VATT_CMD_STATUS_TIMES		=       0x0a12
VATT_CMD_STATUS_SECONDARY1	=       0x0a13
VATT_CMD_STATUS_SECONDARY2	=       0x0a14
VATT_CMD_STATUS_TEMPS		=       0x0a15
VATT_CMD_STATUS_RELAY		=       0x0a16
VATT_CMD_STATUS_CUROBJ		=       0x0a20




class bintelemSQL( Base, logger ):

    __tablename__ = "vatttel_binary_telem"

    id = Column( Integer, primary_key=True )

    elevation = Column(Float, nullable=True)
    azimuth = Column(Float, nullable=True)
    derotator = Column(Float, nullable=True)
    timestamp = Column( DATETIME, nullable=True )

    def __init__( self ):
        logger.__init__( self )
        self.ColumnDescription = OrderedDict(

            elevation = "Altitude/Elevation angle",
            azimuth = "Azimuth Angle (0=North)",
            derotator = "Derotator Angle",
            timestamp = "Timestamp",
        )
        self.description = "Telemetry (mnelson)"


class binrelaySQL( Base, logger ):
    __tablename__ = "vatttel_binary_relay"

    id = Column( Integer, primary_key=True )
    relay01 = Column( Float, nullable=True )
    relay02 = Column( Float, nullable=True )
    relay03 = Column( Float, nullable=True )
    relay04 = Column( Float, nullable=True )
    relay05 = Column( Float, nullable=True )
    relay06 = Column( Float, nullable=True )
    relay07 = Column( Float, nullable=True )
    relay08 = Column( Float, nullable=True )
    relay09 = Column( Float, nullable=True )
    relay10 = Column( Float, nullable=True )
    relay11 = Column( Float, nullable=True )


    timestamp = Column( DATETIME, nullable=True )

    def __init__( self ):
        logger.__init__( self )
        self.ColumnDescription = OrderedDict(

            relay01 = "relay01",
            relay02 = "relay02",
            relay03 = "relay03",
            relay04 = "relay04",
            relay05 = "relay05",
            relay06 = "relay06",
            relay07 = "relay07",
            relay08 = "relay08",
            relay09 = "relay09",
            relay10 = "relay10",
            relay11 = "relay11",
        )
        self.description = "Relays (mnelson)"


class bintempsSQL( Base, logger ):
    __tablename__ = "vatttel_binary_temps"

    id = Column( Integer, primary_key=True )

    #ambient temp
    temp01 = Column( Float, nullable=True )

    #strut temp
    temp02 = Column( Float, nullable=True )

    #Glass temp
    temp03 = Column( Float, nullable=True )

    #Cell temp
    temp04 = Column( Float, nullable=True )
    temp05 = Column( Float, nullable=True )
    temp06 = Column( Float, nullable=True )
    temp07 = Column( Float, nullable=True )
    temp08 = Column( Float, nullable=True )
    temp09 = Column( Float, nullable=True )

    timestamp = Column( DATETIME, nullable=True )




    def __init__( self ):
        logger.__init__( self )
        self.ColumnDescription = OrderedDict(
            temp01 = "Ambient Temperature",
            temp02 = "Strut Temperature",
            temp03 = "Glass Temperature",
            temp04 = "Cell Air Temperature",
            temp05 = "temp05",
            temp06 = "temp06",
            temp07 = "temp07",
            temp08 = "temp08",
            temp09 = "temp09",
        )
        self.description = "Temperature (mnelson)"

class bintelem( getter ):

    socket = None
    logger = bintelemSQL


    def __init__( self ):
        self.current_data = {}


        #get the config information from superclass
        super( bintelem, self ).__init__()



    def open_socket( self ):
        print("opening socket")
        self.socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.socket.settimeout(0.25)

        try:
            self.socket.connect( tuple(self.cfg[ "vatttel_bin_addr" ]) )
            retn = True
        except Exception as err:
            print ( "Could not connect to vatttel" )
            self.socket = None
            retn = False
        return False



    def getdata( self, log=True):
        # Open the socket if its not open
        if self.socket is None:
            self.open_socket()
            return None


        upvals = self.sendrecv( VATT_CMD_STATUS_ALTAZ )
        if upvals is not None:
            self.current_data["azimuth"] = upvals[1]
            self.current_data["elevation"] = upvals[2]
            self.current_data["derotator"] = upvals[3]

        else:
            return None


        upvals = self.sendrecv( VATT_CMD_STATUS_RELAY )
        #I don't remember why I couched these in
        #try/except statements. Probably not necessary
        if upvals is not None:
            pass

            try:
                self.current_data["relay01"] = upvals[1]
            except Exception as err:
                pass
            try:
                self.current_data["relay02"] = upvals[1]
            except Exception as err:
                pass
            try:
                self.current_data["relay03"] = upvals[3]
            except Exception as err:
                pass
            try:
                self.current_data["relay04"] = upvals[4]
            except Exception as err:
                pass
            try:
                self.current_data["relay05"] = upvals[1]
            except Exception as err:
                pass
            try:
                self.current_data["relay06"] = upvals[1]
            except Exception as err:
                pass
            try:
                self.current_data["relay07"] = upvals[3]
            except Exception as err:
                pass
            try:
                self.current_data["relay08"] = upvals[4]
            except Exception as err:
                pass
            try:
                self.current_data["relay09"] = upvals[4]
            except Exception as err:
                pass
            try:
                self.current_data["relay10"] = upvals[4]
            except Exception as err:
                pass
            try:
                self.current_data["relay11"] = upvals[4]
            except Exception as err:
                pass



        upvals = self.sendrecv( VATT_CMD_STATUS_TEMPS )
        self.current_data["temp01"] = upvals[1]
        self.current_data["temp02"] = upvals[2]
        self.current_data["temp03"] = upvals[3]
        self.current_data["temp04"] = upvals[4]
        self.current_data["temp05"] = upvals[5]
        self.current_data["temp06"] = upvals[6]
        self.current_data["temp07"] = upvals[7]
        self.current_data["temp08"] = upvals[8]
        self.current_data["temp08"] = upvals[9]


        if log:

            self.to_sql( self.current_data )

        return self.current_data


    def to_sql(self, data):
        bt = bintelemSQL()
        bt.load_data( data )
        bt.log()

        br = binrelaySQL()
        br.load_data( data )
        br.log()

        btemps = bintempsSQL()
        btemps.load_data( data )
        btemps.log()



    def sendrecv( self, cmd ):

        cmd = self.pack_cmd( cmd )

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


    def pack_cmd( self, command ):
        return "VATT\x00".encode() + struct.pack('b', ( command >> 16) & 0xFF) + struct.pack('b', (command >> 8) & 0xFF ) + struct.pack( 'b', command & 0xFF )


    def unpack_resp( self, pkt ):
        """The response from the mnelson server is 64 network order bytes of
        unsigned short integers in micro arcseconds (1/3600000.0). """
        vals = [ val/3600000.0 for val in struct.unpack('!16i', pkt) ]

        #the first two bytes are the header "VATT"
        return vals[2:]




