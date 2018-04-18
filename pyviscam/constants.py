#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file contains the constants value for camera
For now, these are Tandberg/Cisco, but we need a better system
to choose the model of camera, and the constants and features only for this one
"""

commands = {
            'AE_mode':
                {'getcmd'    : "\x04\x39",
                 "gettype"   : "enum",
                 "getattr"   : {0: 'auto', 3: 'manual'},
                 'setcmd'   : "\x01\x04\x39",
                 'settype'  : 'enum',
                 'setattr'  : {'auto' : '\x00','manual' : '\x03'}
                },
            'als_bgain':
                {'getcmd'    : "\x50\x51",
                 "gettype"   : "uint32"
                },
            'als_ggain':
                {'getcmd'    : "\x50\x52",
                 "gettype" : "uint32"
                },
            'als_rgain':
                {'getcmd'    : "\x50\x50",
                 "gettype" : "uint32"
                },
            'als_wgain':
                {'getcmd'    : "\x50\x53",
                 "gettype" : "uint32"
                },
            'backlight':
                {'getcmd'    : "\x04\x33",
                 "gettype" : "enum",
                 "getattr"   : {2: 'on', 3: 'off', 4: 'auto'},
                 'setcmd'    : "\x01\x04\x33",
                 'settype'   : 'enum',
                 'setattr'   : {'on' : '\x02','off' : '\x03'},
                 'description': "BacklightCompensation Mode"
                },
            'call_led':
                {'getcmd'   : "\x01\x33\x01",
                 "gettype"  : "enum",
                 "getattr"  : {2: 'on', 3: 'off', 4: 'blink'},
                 'setcmd'   : "\x01\x33\x01",
                 'settype'  : 'enum',
                 'setattr'  : {'on' : '\x01','off' : '\x00', 'blink': '\x02'}
                },
            'debug':
                {'setcmd'   : "\x01\x39",
                 'settype'  : 'enum',
                 'setattr'  : {'on' : '\x01','off' : '\x00', }
                },
            'debug_cmd':
                 {'setcmd'   : "\xa4",
                 'settype'  : 'debug',
                },
            'flip':
                {'getcmd'    : "\x04\x66",
                 "gettype"   : "enum",
                 "getattr"   : {2: "flipped", 3: "normal"},
                 'setcmd'    : "\x01\x04\x66",
                 'settype'   : 'enum',
                 'setattr'   : {'flipped' : '\x02','normal' : '\x03', 'flip': '\x02'},
                 'description': 'flip image'
                },
            'focus_mode':
                {'getcmd'    : "\x04\x38",
                 "gettype"   : "enum",
                 "getattr"   : {2: 'auto', 3: 'manual'},
                 'setcmd'    : "\x01\x04\x38",
                 'settype'   : 'enum',
                 'setattr'   : {'auto' : '\x02','manual' : '\x03'},
                 'description': 'Focus mode.'
                },
            'focus':
                {'getcmd'    : "\x04\x48",
                 "gettype"   : "int16",
                 'setcmd'    : "\x01\x04\x48",
                 'settype'   : 'int16',
                 'setmin'    : 4095,
                 'setmax'    : 4673,
                 'description':'Focus Direct (Near: 4096.. Tele: 4672)'
                },
            'focus_ctl':
                {'setcmd'    : "\x01\x04\x08",
                 'settype'   : 'enum',
                 'setattr'   : {'stop' : '\x00','far_slow' : '\x2a','far_fast' : '\x2b','near_slow' : '\x3a','near_fast' : '\x3b'},
                 'description':'Focus Direct'
                },
            'gamma_mode':
                {'getcmd'    : "\x04\x51",
                 "gettype"   : "enum",
                 "getattr"   : {2: 'auto', 3: 'manual'},
                 'setcmd'    : "\x01\x04\x51",
                 'settype'   : 'enum',
                 'setattr'   : {'auto' : '\x02','manual' : '\x03'},
                 'description': 'Gamma mode. Default uses gamma table 4'
                },
            'gamma_table':
                {'getcmd'    : "\x04\x52",
                 "gettype"   : "int16",
                 'setcmd'    : "\x01\x04\x52",
                 'settype'   : 'int16',
                 'setmin'    : 0,
                 'setmax'    : 7,
                 'description': 'Gamma table. 0..7, default 4'
                },
            'gain':
                {'setcmd'    : "\x01\x04\x4c",
                 'settype'   : 'int16',
                 'setmin'    : 12,
                 'setmax'    : 21,
                 'description' : "Gain position, values: 12-21dB, only if AE mode manual"
                },
            'hwid':
                {'getcmd'    : "\x04\x24",
                 "gettype" : "string"
                },
            # 'id':
            #     {'getcmd'    : "\x04\x22",
            #      "gettype" : "id"
            #     },
            'iris':
                {'setcmd'    : "\x01\x04\x75",
                 'settype'   : 'int16',
                 'setmin'    : 0,
                 'setmax'    : 40,
                 'description' : "Iris position, range 0..50, only if AE mode manual"
                },
            'IR_receive':
                {'getcmd'    : "\x06\x08",
                 "gettype"   : "enum",
                 "getattr"   : {2: 'on', 3: 'true'}
                },
            'mirror':
                {'getcmd'    : "\x04\x61",
                 "gettype"   : "enum",
                 "getattr"   : {2: 'reversed', 3: 'normal'},
                 'setcmd'    : "\x01\x04\x61",
                 'settype'   : 'enum',
                 'setattr'   : {'reversed' : '\x02','normal' : '\x03', 'mirror': '\x02'},
                 'description': 'Mirror image'
                },
            'motor_moved':
                {'setcmd'   : "\x01\x50\x30",
                 'settype'  : 'enum',
                 'setattr'  : {'on': "\x01", 'off': "\x00"},
                 'description':'Motor movement detection, detect and reset position if on'
                },
            'pan_tilt':
                {'getcmd'    : "\x06\x12",
                 "gettype"   : "int16int16",
                 'setcmd'    : "\x01\x06\x02\x01\x01",
                 'settype'   : "int16int16",
                 'description':'pan tilt direct control'
                },
            'pan_tilt_ctl':
                {'setcmd'    : "\x01\x06",
                 'settype'   : 'enum',
                 'setattr'   : {    'stop'      : '\x01\x03\x03\x03\x03',
                                    'reset'     : '\x05',
                                    'up'        : '\x01\x03\x03\x03\x01',
                                    'down'      : '\x01\x03\x03\x03\x02',
                                    'left'      : '\x01\x03\x03\x01\x03',
                                    'right'     : '\x01\x03\x03\x02\x03',
                                    'up_left'   : '\x01\x03\x03\x01\x01',
                                    'up_right'  : '\x01\x03\x03\x02\x01',
                                    'down_left' : '\x01\x03\x03\x01\x02',
                                    'down_right': '\x01\x03\x03\x02\x02',
                                },
                 'description':'Pan Tilt Controller'
                 },
            'power_led':
                {'getcmd'   : "\x01\x33\x02",
                 "gettype"  : "enum",
                 "getattr"  : {2: 'on', 3: 'off'},
                 'setcmd'   : "\x01\x33\x02",
                 'settype'  : 'enum',
                 'setattr'  : {'on': "\x01", 'off': "\x00"}
                },
            'power':
                {'getcmd'    : "\x04\x00",
                 "gettype"   : "enum",
                 "getattr"   : {2: 'on', 3: 'off'},
                 'setcmd'    : "\x01\x04\x00",
                 'settype'   : 'enum',
                 'setattr'   : {'on': "\x02", 'off': "\x03"}
                },
            'swid':
                {'getcmd'    : "\x04\x23",
                 "gettype" : "string"
                },
            'upside_down':
                {'getcmd'    : "\x50\x70",
                 "gettype" : "enum",
                 "getattr"   : {2: 'no', 3: 'yes'}
                },
            'version':
                {'getcmd'    : "\x00\x02",
                },
            'video':
                {'getcmd'    : "\x06\x23",
                 "gettype"   : "enum16",
                 "getattr"   : {0: '1080p25', 1: '1080p30', 2: '1080p50', 3: '1080p60', 4: '720p25', 5: '720p30', 6: '720p50', 7: '720p60'},
                 'setcmd'    : "\x01\x35\x00",
                 'settype'   : 'enum',
                 'setattr'   : {'1080p25': '\x00\x00',  '1080p30': '\x00\x01', '1080p50': '\x00\x02',  '1080p60': '\x00\x03',  '720p25': '\x00\x04',  '720p30': '\x00\x05',  '720p50': '\x00\x06',  '720p60': '\x00\x07'}
                },
            'WB_mode':
                {'getcmd'    : "\x04\x35",
                 "gettype"   : "enum",
                 "getattr"   : {2: 'auto', 6: 'table'},
                 'setcmd'    : "\x01\x04\x35",
                 'settype'   : 'enum',
                 'setattr'   : {'auto' : '\x00','table' : '\x06'}
                },
            'WB_table':
                {'getcmd'    : "\x04\x75",
                 "gettype"   : "int16",
                 'setcmd'    : "\x01\x04\x75",
                 'settype'   : 'int16',
                },
            'zoom':
                {'getcmd'    : "\x04\x47",
                 "gettype"   : "int16",
                 'setcmd'    : "\x01\x04\x47",
                 'settype'   : 'int16',
                 'setmin'    : 0,
                 'setmax'    : 2885,
                 'description':'Zoom Direct (Wide: 0.. Tele: 2885)'
                },
            'zoom_ctl':
                {'setcmd'    : "\x01\x04\x07",
                 'settype'   : 'enum',
                 'setattr'   : {'stop' : '\x00','tele_slow' : '\x2a','tele_fast' : '\x2b','wide_slow' : '\x3a','wide_fast' : '\x3b'},
                 'description':'Zoom Controller'
                },

}
            # 'aperture':     "\x04\x42",
            # 'bright':       "\x04\x4D",
            # 'chromasuppress':"\x04\x5F",
            # 'color_gain':   "\x04\x49",
            # 'color_hue':    "\x04\x4F",
            # 'condition':    "\x06\x34",
            # 'expo_compensation_amount':"\x04\x4E",
            # 'expo_compensation':"\x04\x3E",
            # 'fan':          "\x7E\x01\x38",
            # 'FX':           "\x04\x63",
            # 'gain_blue':    "\x04\x44",
            # 'gain_limit':   "\x04\x2C",
            # 'gain_red':     "\x04\x43",
            # 'gain':         "\x04\x4C",
            # 'gamma':        "\x04\x5B",
            # 'high_sensitivity':"\x04\x5E",
            # 'HR':           "\x04\x52",
            # 'info_display': "\x7E\x01\x18",
            # 'IR_auto_threshold':"\x04\x21",
            # 'IR_auto':      "\x04\x51",
            # 'IR_receive':   "\x06\x08",
            # 'IR':           "\x04\x01",
            # 'iris':         "\x04\x4B",
            # 'NR':           "\x04\x53",
            # 'pan_tilt_mode':"\x06\x10",
            # 'pan_tilt_speed':"\x06\x11",
            # 'shutter':      "\x04\x4A",
            # 'slowshutter':  "\x04\x5A",
            # 'video_next':   "\x06\x33",
            # 'WD':           "\x04\x3D",
            # 'zoom_digital': "\x04\x06",
            # 'focus_auto_mode':"\x04\x57",
            # 'focus_auto_sensitivity':"\x04\x58",
            # 'focus_ir':     "\x04\x11",
            # 'focus_nearlimit':"\x04\x28",

#
# getattrs = {
#             'AE':           {0: 'auto', 3: 'manual', 10: 'shutter', 11: 'iris', 13: 'bright'},
#             'backlight':    {2: 'On', 3: 'Off', 4: 'Auto'},
#             'call_led':     {2: 'On', 3: 'Off', 4: 'Blink'},
#             'flip':         {2: True, 3: False},
#             'focus_auto':   {2: True, 3: False},
#             'IR_receive':   {2: True, 3: False},
#             'mirror':       {2: True, 3: False},
#             'power_led':    {2: True, 3: False},
#             'power':        {2: True, 3: False},
#             'upside_down':  {0: False, 1: True},
#             'video':        {0: '1080p25', 1: '1080p30', 2: '1080p50', 3: '1080p60', 4: '720p25', 5: '720p30', 6: '720p50', 7: '720p60'},
#             'WB':           {0: 'auto', 1: 'indoor', 2: 'outdoor', 3: 'trigger', 5: 'manual'},
#             #                     12:300, 11:215, 10:150, 9:120, 8:100, 7:75, 6:50, 5:25, 4:12, 3:6, 2:3, 1:2, 0:1},
#             #                     17:1750, 16:1250 , 15:1000, 14:600, 13:425,
#             # 'expo_compensation_amount':{14:10.5, 13:9, 12:7.5, 11:6, 10:4.5, 9:3, 8:1.5, 7:0, 6:-1.5, 5:-3, 4:-4.5, 3:-6, 2:-7.5, 1:-9, 0:-10.5}, \
#             # 'expo_compensation':{2:True,3:False},
#             # 'fan':          {0:True, 1:False},
#             # 'focus_auto_mode':{0:'normal', 1:'interval', 2:'zoom_trigger'},
#             # 'focus_auto_sensitivity':{2:'normal', 3:'low'},
#             # 'focus_ir':     {2:True,3:False},
#             # 'FX':           {0:'normal', 2:'negart', 4:'BW'},
#             # 'gain_limit':   {4:+6, 5:+8, 6:+10, 7:+12, 8:+14, 9:+16, 10:+18, 11:+20, 12:+22, 13:+24, 14:+26, 15:+28}, \
#             # 'gain':         {0:-3, 1:0, 3:+2, 3:+4, 4:+6, 5:+8, 6:+10, 7:+12, 8:+14, 9:+16, 10:+18, 11:+20, 12:+22, 13:+24, 14:+26, 15:+28}, \
#             # 'high_sensitivity':{2:True,3:False},
#             # 'HR':           {2:True,3:False},
#             # 'info_display': {2:True,3:False},
#             # 'IR_auto':      {2:True,3:False},
#             # 'IR':           {2:True,3:False},
#             # 'iris':         {17:1.6, 16:2, 15:2.4, 14:2.8, 13:3.4, 12:4, 11:4.8, 10:5.6, 9:6.8, 8:8, 7:9.6, 6:11, 5:14, 0:0},
#             # 'shutter':      {21:10000, 20:6000, 19:3500, 18:2500,
#             # 'slowshutter':  {2:'auto', 3:'manual'},
#             # 'video_next':   {0:'1080i59.95', 1:'1080p29.97', 2:'720p59.94', 3:'720p29.97', 4:'NTSC', 8:'1080i50', 9:'720p50', 10:'720p25', 11:'1080i50', 12:'PAL'},
#             # 'WD':           {2:True,3:False},
#             # 'zoom_digital': {2:True,3:False},
#             # 'video':        {0:'1080i59.95', 1:'1080p29.97', 2:'720p59.94', 3:'720p29.97', 4:'NTSC', 8:'1080i50', 9:'720p50', 10:'720p25', 11:'1080i50', 12:'PAL'}, \
#
#             }

# high_res_params = ['shutter', 'iris', 'gain', 'gain_limit', 'gain_red', 'gain_blue',
#     'bright', 'expo_compensation_amount', 'aperture', 'IR_auto_threshold']
#
# very_high_res_params = ['zoom', 'focus',
#     'focus_nearlimit', 'focus_auto_interval', 'ID']
