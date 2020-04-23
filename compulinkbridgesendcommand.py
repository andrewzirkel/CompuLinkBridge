import os
import sys
import optparse
import compulink


def main(argv):
    p = optparse.OptionParser()
    p.set_usage("""Usage: %prog [options] verb""")
    p.add_option("-a", "--address")
    p.add_option("-c", "--command")
    p.add_option("-d", "--debug", type=int, default=0)
    options, argv = p.parse_args(argv)

    compulinkTargetAddress = options.address
    if not compulinkTargetAddress:
        print >> sys.stderr, p.get_usage()
        return 1
    compulinkCommand = options.command
    if not compulinkCommand:
        print >> sys.stderr, p.get_usage()
        return 1

    compulinkTargetAddress = int(compulinkTargetAddress)
    compulinkCommand = int(compulinkCommand)

    #setup compulink
    mycompulink = compulink.CompuLink(18, compulinkTargetAddress)
    mycompulink.debug = options.debug

    mycompulink.sendCommand(compulinkCommand)
    mycompulink.cleanup()


if __name__ == "__main__":
    sys.exit(main(sys.argv))

