import sys
import optparse
import harmony


def main(argv):
    myharmony = harmony.Harmony()
    myharmony.listen()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
