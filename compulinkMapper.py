import os
import sys
import optparse
import compulink
import time


def main(argv):
    # setup compulink
    mycompulink = compulink.CompuLink(18, 1)
    mycompulink.debug = 1
    for address in range(1,16):
        mycompulink.address = address
        for command in range(1,16):
            mycompulink.sendCommand(command)
            time.sleep(3)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
