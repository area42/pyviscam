#!/usr/bin/env python
#
# import modules used here -- sys is a very standard one
import sys, argparse, logging
from pyviscam.broadcast import Viscam, Camera
from pyviscam.port import listports

def describe(cam,c):
      print c.ljust(12),
      if cam.setter(c):
          print " set",
      else:
          print "    ",
      if cam.getter(c):
          print " get",
      else:
          print "    ",
      if cam._hasattr(c,"settype"):
          print cam._getattr(c,"settype").rjust(10),
      else:
          print "".rjust(10),
      print " %s" % cam.describe(c),
      opts = cam.keys(c)
      if opts:
          print "(",
          print ','.join(opts),
          print ")",
      print ''

# Gather our code in a main() function
def main(args, loglevel):
  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

  #cams = Viscam(port=args.port)
  cam  = Camera(None,port=args.port,id=1)

  cmd = args.command

  if cmd == "list" or cmd == "help":
    lc = sorted(cam.allcmds(),key=lambda s: s.lower())
    for c in lc:
        describe(cam,c)
  elif args.args:  # there are args lets assume they are inputs to a setters
    arglist = args.args
    arg = arglist[0]
    if cam.exists(cmd):
        if (arg == "help" or arg == "?") and cmd != "debug_cmd":
            print describe(cam,cmd)
        else:
            if len(arglist) == 2:
                ret = cam._set(cmd,arg,arglist[1])
            else:
                ret = cam._set(cmd,arg)
            if cam.getter(cmd):
                print cam._get(cmd)
    else:
        logging.error("No such command %s ",cmd)
  else:
    if cam.getter(cmd):
        print cam._get(cmd)
    else:
        logging.error("No such query %s ",cmd)

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  parser = argparse.ArgumentParser(
        description = "Sends commands and queries to attached VISCA camera",
        epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
                fromfile_prefix_chars = '@' )
  # TODO Specify your real parameters here.
  parser.add_argument("command",
                      help = "command to send",
                      metavar = "command")
  parser.add_argument("args",
                      nargs=argparse.REMAINDER,
                      help = "optional command arguments",
                      metavar = "args")
  parser.add_argument("-v",
                      "--verbose",
                      help="increase output verbosity",
                      action="store_true")
  ports = listports()
  if len(ports) == 0:
      parser.add_argument("-p",
                        "--port",
                        required=True,
                        help="specify serial port the camera(s) is connected to")
  else:
      parser.add_argument("-p",
                        "--port",
                        default=ports[0],
                        help="specify serial port the camera(s) is connected to (default = %s)" % ports[0])

  args = parser.parse_args()

  # Setup logging
  if args.verbose:
    loglevel = logging.DEBUG
  else:
    loglevel = logging.INFO

  main(args, loglevel)
