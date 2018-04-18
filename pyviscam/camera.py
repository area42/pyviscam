#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file contains the Camera class that represent a camera device
You don't have to create this class by yourself as it is done for each device
that answers to a broadcast message.

"""
from pyviscam.port import Serial
# from pyviscam.convert import hex_to_int, i2v, scale
# from pyviscam.pan_tilt_utils import degree_to_visca, visca_to_degree
from pyviscam.constants import commands

from pyviscam import debug
import hexdump
import re
import logging,sys

class Camera(object):
    """
    create a visca camera
    """
    def __init__(self, parent, port=None,id=1):
        """the constructor"""
        if port==None:
            self.serial = parent.serial
            self.parent = parent
            logging.debug("new visca camera")
        else:
            serial = Serial()
            self.serial = serial
            self.port = port
            self.id   = id
            if not self.serial.open(port):
                logging.error("Failed to open port %s, bailing",port)
                return None

    def __getattr__(self, name):
        cmdget = self._get(name)
        if cmdget == None:
            return super(Camera, self).__getattr__(name, value)
        else:
            return cmdget

    def __setattr__(self, name, value,value2=None):
        cmdset = self._set(name,value,value2)
        if cmdset == None:
            super(Camera, self).__setattr__(name, value)
        else:
            return cmdset

    def exists(self,name):
        return name in commands

    def describe(self,name):
        if self.exists(name) and 'description' in commands[name]:
            return commands[name]['description']
        else:
            return ''

    def _filter(self,key):
        return [ a for a in commands if key in commands[a]]

    def _hasattr(self,name,key):
        return name in commands and key in commands[name]

    def _getattr(self,name,key):
        if self._hasattr(name,key):
            return commands[name][key]
        return None

    def getters(self):
        return self._filter('getcmd')

    def getter(self,name):
        return self._hasattr(name,'getcmd')

    def setters(self):
        return self._filter('setcmd')

    def setter(self,name):
        return self._hasattr(name,'setcmd')

    def keys(self,name):
        if self._hasattr(name,'setattr'):
            return [ k for k in commands[name]['setattr']]
        else:
            return None

    def allcmds(self):
        return [ k for k in commands ]

    def _send_packet(self, data, recipient=1):
        """
        according to the documentation:

        |------packet (3-16 bytes)---------|

         header     message      terminator
         (1 byte)  (1-14 bytes)  (1 byte)

        | X | X . . . . .  . . . . . X | X |

        header:                  terminator:
        1 s2 s1 s0 0 r2 r1 r0     0xff

        with r,s = recipient, sender msb first

        for broadcast the header is 0x88!

        we use -1 as recipient to send a broadcast!

        """
        # we are the controller with id=0
        sender = 0
        if recipient == -1:
            # broadcast
            rbits = 0x8
        else:
            # the recipient (address = 3 bits)
            rbits = recipient & 0b111
        sbits = (sender & 0b111)<<4
        header = 0b10000000 | sbits | rbits
        terminator = 0xff
        packet = chr(header)+data+chr(terminator)
        logging.debug("Send: %s" % hexdump.dump(packet))
        self.serial.mutex.acquire()
        self.serial._write_packet(packet)
        reply = self.serial.recv_packet()
        logging.debug("Received: %s" % hexdump.dump(reply))
        if reply:
            if reply[-1:] != '\xff':
                logging.warning("ERROR 41 - received packet not terminated correctly: %s" % reply.encode('hex'))
                reply = None
            self.serial.mutex.release()
            return reply
        else:
            return None

    def _cmd_cam_alt(self, subcmd):
        """
        shortcut to send command with alternative prefix
        """
        prefix = '\x01\x06'
        self._cmd_cam(subcmd, prefix)

    def _cmd_cam(self, subcmd, prefix=''):
        """
        Send a command to the camera and return the answer
        The camera answer first an acceptation of the command, and then a completion
        If the command cannot be send or is not a valide command
        => the camera will answers an error code
        """
        packet = prefix + subcmd
        reply = self._send_packet(packet)

        if reply.startswith('\x90'+'\x50'):
            if reply[-4:] == '\x00\xFF':
                debugout = reply[4:][:-4].decode('hex')
                logging.debug(debugout)
            logging.debug('-----------COMMAND COMPLETE-------------------')
            return True
        if reply.startswith('\x90'+'\x90'):
            debugout = reply[2:][:-2]
            logging.debug(debugout)
            try:
                while True:
                    reply = self.serial.recv_packet()
                    debugout = reply[2:][:-2]
                    logging.debug(debugout)
            except TimeoutError:
                logging.debug('timed out')
            logging.debug('-----------COMMAND COMPLETE 9090-------------------')
            return True
        if reply == '\x90'+'\x41'+'\xFF':
            logging.debug('-----------ACK 1-------------------')
            reply = self.serial.recv_packet()
            if reply == '\x90'+'\x51'+'\xFF':
                logging.debug('--------COMPLETION 1---------------')
                return True
        elif reply == '\x90'+'\x42'+'\xFF':
            logging.debug('-----------ACK 2-------------------')
            reply = self.serial.recv_packet()
            if reply == '\x90'+'\x52'+'\xFF':
                logging.debug('--------COMPLETION 2---------------')
                return True
        elif reply == '\x90'+'\x60'+'\x02'+'\xFF':
            logging.warning('--------Syntax Error------------')
            return False
        elif reply == '\x90'+'\x60'+'\x41'+'\xFF':
            logging.warning('-----------ERROR 3 (not in this mode)------------')
            return False
        elif reply == '\x90'+'\x61'+'\x41'+'\xFF':
            logging.warning('-----------ERROR 1 (not in this mode)------------')
            return False
        elif reply == '\x90'+'\x62'+'\x41'+'\xFF':
            logging.warning('-----------ERROR 2 (not in this mode)------------')
            return False

    def _come_back(self, query):
        """
        Send a query and wait for (ack + completion + answer)
            :Accepts a visca query (hexadeciaml)
            :Return a visca answer if ack and completion (hexadeciaml)
        """
        # send the query and wait for feedback
        reply = self._send_packet(query)
        if reply == '\x90'+'\x60'+'\x03'+'\xFF':
            logging.info('-------- FULL BUFFER ---------------')
            # buffer is full, send it again
            self._come_back(query)
        elif reply.startswith('\x90'+'\x50'):
            logging.debug('-------- QUERY COMPLETION ---------------')
            # We know this is a valid query request, please send it back
            return reply
        elif reply == '\x90'+'\x60'+'\x02'+'\xFF':
            logging.error('-------- QUERY SYNTAX ERROR ---------------')
            return False
        elif reply == '\x90'+'\x60'+'\x41'+'\xFF':
            logging.warning('-----------ERROR 3 (not in this mode)------------')
            return False
        elif reply == '\x90'+'\x61'+'\x41'+'\xFF':
            logging.warning('-----------ERROR 1 (not in this mode)------------')
            return False
        elif reply == '\x90'+'\x62'+'\x41'+'\xFF':
            logging.warning('-----------ERROR 2 (not in this mode)------------')
            return False


    def parse_string(self,hexreply):
        return re.sub(r'^.050(.*)ff$',r'\1',hexreply).decode('hex')

    def parse_int4(self,hexreply):
        return int(re.sub(r'^.050.(.)ff',r'0x\1',hexreply),0)

    def parse_int16(self,hexreply):
        return int(re.sub(r'^.050.(.).(.).(.).(.)ff',r'0x\1\2\3\4',hexreply),0)

    def parse_int32(self,hexreply):
        return  int(re.sub(r'^.050.(.).(.).(.).(.).(.).(.).(.).(.)ff',r'0x\1\2\3\4\5\6\7\8',hexreply),0)

    def parse_int16int16(self,hexreply):
        return (int(re.sub(r'^.050.(.).(.).(.).(.).(.).(.).(.).(.)ff',r'0x\1\2\3\4',hexreply),0),
                int(re.sub(r'^.050.(.).(.).(.).(.).(.).(.).(.).(.)ff',r'0x\5\6\7\8',hexreply),0))

    def _get(self, function=None):
        """
        _get method needs a parameter as argument
            :Return False if no parameter is provided
            :Return False if parameter provided does not exist
            :Return
        """
        if not function in commands:
            return None

        logging.debug('QUERY: %s', function)

        # transform the property into its code (located in the __init__file of the package)
        if function in commands:
            if 'getcmd' in commands[function]:
                subcmd = commands[function]['getcmd']
            else:
                logging.debug('ERROR XX - function %s has no getter',function)
                return False
        else:
            if debug:
                # there is no code for this function
                logging.debug('ERROR XX - function %s is not implemented',function)
            return False
        # query starts with '\x09'
        query = '\x09' + subcmd

        # wait for the reply
        if len(subcmd) > 0:
            reply = self._come_back(query)
        else:
            reply = self.serial.recv_packet()
        if reply:

            hexreply = reply.encode('hex')
            reply_type = commands[function]['gettype']

            if reply_type == 'enum':
                return commands[function]['getattr'][self.parse_int4(hexreply)]
            elif reply_type == 'enum16':
                return commands[function]['getattr'][self.parse_int16(hexreply)]
            elif reply_type == 'int16':
                return self.parse_int16(hexreply)
            elif reply_type == 'int32':
                return self.parse_int32(hexreply)
            elif reply_type == 'int16int16':
                return self.parse_int16int16(hexreply)
            elif reply_type == 'string':
                return self.parse_string(hexreply)
            else:
                logging.error('FIX ME : is it normal that %s with type %s has no translation??' , function,reply_type )

    # def parse_string(self,hexreply):
    #     return re.sub(r'^.050(.*)ff$',r'\1',hexreply).decode('hex')
    #
    # def parse_int4(self,hexreply):
    #     return int(re.sub(r'^.050.(.)ff',r'0x\1',hexreply),0)

    def encode_int16(self,value):
        hv = "%0.4X" % value
        hs = "0%c0%c0%c0%c" % (hv[0],hv[1],hv[2],hv[3])
        return hs.decode('hex')

    # def parse_int32(self,hexreply):
    #     return  int(re.sub(r'^.050.(.).(.).(.).(.).(.).(.).(.).(.)ff',r'0x\1\2\3\4\5\6\7\8',hexreply),0)
    #
    # def parse_int16int16(self,hexreply):
    #     return (int(re.sub(r'^.050.(.).(.).(.).(.).(.).(.).(.).(.)ff',r'0x\1\2\3\4',hexreply),0),
    #             int(re.sub(r'^.050.(.).(.).(.).(.).(.).(.).(.).(.)ff',r'0x\5\6\7\8',hexreply),0))

    def _set(self, function,value,value2=None):
        """
        _set method needs a function name and value as argument
            :Return None if function not in commands
            :Return False if value was not set
            :Return True if value was set

            :Raises NotImplementedError if setter doesn't exist for function
            :Raises ValueError if value out of range or not defined
        """

        if not function in commands:
            return None

        logging.debug("setter: %s",function)

        if function in commands:
            if 'setcmd' in commands[function]:
                subcmd = commands[function]['setcmd']
            else:
                logging.error('setter: %s not implemented ',function,value)
                raise NotImplementedError('setter: %s not implemented ' % function)

        settype = commands[function]['settype']
        if settype == 'enum':
            if value in commands[function]['setattr']:
                cmd = subcmd + commands[function]['setattr'][value]
            else:
                logging.error('setter: %s key %s not found in setattr ',function,value)
                raise ValueError("setter: %s key '%s' not found in setattr" % (function,value))

        elif settype == 'int16':
            value = int(value)
            if 'setmin' in commands[function] and value < commands[function]['setmin']:
                logging.error('setter: %s value %d < min (%d)',function,value,commands[function]['setmin'])
                raise ValueError("value %s out of range (min)" % function)
            if 'setmax' in commands[function] and value > commands[function]['setmax']:
                logging.error('setter: %s value %d > max (%d)',function,value,commands[function]['setmax'])
                raise ValueError("value %s out of range (max)" % function)
            cmd = subcmd + self.encode_int16(value)

        elif settype == 'int16int16':
            value = int(value)
            if value2 == None:
                logging.error('setter: %s value2 not provided for int16int16',function)
                raise ValueError("%s value2 not provided for int16int16" % function)
            value2 = int(value2)
            if 'setmin' in commands[function] and value < commands[function]['setmin']:
                logging.error('setter: %s value %d < min (%d)',function,value,commands[function]['setmin'])
                raise ValueError("value %s out of range (min)" % function)
            if 'setmax' in commands[function] and value > commands[function]['setmax']:
                logging.error('setter: %s value %d > max (%d)',function,value,commands[function]['setmax'])
                raise ValueError("value %s out of range (max)" % function)
            if 'setmin1' in commands[function] and value < commands[function]['setmin2']:
                logging.error('setter: %s value %d < min (%d)',function,value,commands[function]['setmin2'])
                raise ValueError("value %s out of range (min)" % function)
            if 'setmax2' in commands[function] and value > commands[function]['setmax2']:
                logging.error('setter: %s value %d > max (%d)',function,value,commands[function]['setmax2'])
                raise ValueError("value %s out of range (max)" % function)
            cmd = subcmd + self.encode_int16(value)+self.encode_int16(value2)

        elif settype == 'debug':
            logging.debug("sending debug %s",value)
            cmd = subcmd + value+'\x0d\x00'
            print self._cmd_cam(cmd)
            try:
                while True:
                    reply = self.serial.recv_packet(line_end = True)
                    if reply[:2] == "\x90\x90":
                        reply = reply[2:]
                    if reply[-2:] == "\x00\xff":
                        reply = reply[:-2]
                    sys.stdout.write(reply)
            except RuntimeError:
                    logging.debug('timed out')
            return

        # elif settype == 'int32':
        #     return self.parse_int32(hexreply)
        # elif settype == 'int16int16':
        #     return self.parse_int16int16(hexreply)
        # elif settype == 'string':
        #     return self.parse_string(hexreply)
        else:
            logging.error('setter: %s type %s not implemented ',function,settype)
            raise NotImplementedError('setter: %s type %s not implemented ' % function)

        logging.debug("sending cmd %s" % cmd.encode('hex'))

        return self._cmd_cam(cmd)

    # def home(self):
    #     if debug:
    #         print('home')
    #     subcmd = '\x04'
    #     return self._cmd_cam_alt(subcmd)
    #
    # def reset(self):
    #     if debug:
    #         print('reset')
    #     subcmd = '\x05'
    #     return self._cmd_cam_alt(subcmd)
