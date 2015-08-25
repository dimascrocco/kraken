#
# This is a kraken that handles many hydrometers.
#
# data format: 24442D2C279342741F168D207D41680200724A79F7D2B41B0F005200000052000000241A27
#

import serial
import sys
import collections
import random
from time import strftime
import datetime
import time, threading
from ship import mail


_HEADER = "24442D" # message header
_TIMER = 60.0 * 1 # one minute -> 1 * 60 seconds
_TARGET = "krakenvich@gmail.com


bag = dict()

def store():
    print "###### Storing file..."
    f = open('kraken.dat', 'w')
    for k, v in bag.iteritems():
        f.write(k+ ";" + v + '\n')	
    f.close()
    

    timer = threading.Timer(_TIMER, store)
    timer.daemon = True
    timer.start()
    mail(_TARGET,
        "Kraken Data",
        "Information attached.",
        "kraken.dat")
    


def processData(data):
    print "- processing data: " + data
    
    id = data[2:10] # TODO uncomment for real data stuff
    # id = random.choice(["12345678", "87654321", "12348765", "43215678"])
    print "id: " + id
    bag[id] = _HEADER + data + ";" + strftime("%Y%m%d %H:%M:%S")
    #print "bag -> "
    #print bag

print ".:. Kraken v.0.1 .:." 

#for arg in sys.argv:
#    print "arg = " + arg

print "- parameters: " + str(len(sys.argv))

print """
                        ___
                     .-'   `'.
                    /         }
                    |         ;
                    |         |           ___.--,
           _.._     |0) ~ (0) |    _.---'`__.-( (_.
    __.--'`_.. '.__.\    '--. \_.-' ,.--'`     `''''`
   ( ,.--'`   ',__ /./;   ;, '.__.'`      __
   _`) )  .---.__.' / |   |\   \__..--''''  ''''''--.,_
  `---' .'.''-._.-'`_./  /\ '.  \ _.-~~~````~~~-._`-.__.'
        | |  .' _.-' |  |  \  \  '.               `~---`
         \ \/ .'     \  \   '. '-._)
          \/ /        \  \    `=.__`~-.
          / /\         `) )    / / `''''.
    , _.-'.'\ \        / /    ( (     / /
     `--~`   ) )    .-'.'      '.'.  | (
            (/`    ( (`          ) )  '-;
             `      '-;         (-'

   release the KRAKEN!
"""

timer = threading.Timer(_TIMER, store)
timer.daemon = True
timer.start()

port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=3.0)

hBuffer = collections.deque(maxlen=6)

while True:
    # port.write("\r\nSay something:")
    c = port.read()

    # 24442D (message header)
    hBuffer.append(c)
    header = ''.join(hBuffer)

    if header == _HEADER:
	print "# header found..."
        hBuffer.clear()
        data = port.read(68)
        processData(data)


