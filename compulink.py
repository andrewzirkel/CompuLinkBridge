import os
import RPi.GPIO as GPIO
import time


class CompuLink(object):

    def __init__(self, pin, address=None):
        self.debug = 0
        self.pin = pin
        self.address = address
        # setup GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)

    def cleanup(self):
        # cleanup GPIO
        GPIO.cleanup()

    def pulse0(self):
        if self.debug > 1:
            print "pulsing 0"
        GPIO.output(self.pin, 1)
        time.sleep(.005)
        GPIO.output(self.pin, 0)
        time.sleep(.005)

    def pulse1(self):
        if self.debug > 1:
            print "pulsing 1"
        GPIO.output(self.pin, 1)
        time.sleep(.005)
        GPIO.output(self.pin, 0)
        time.sleep(.015)

    def pulseStop(self):
        if self.debug > 1:
            print "pulsing stop"
        GPIO.output(self.pin, 1)
        time.sleep(.005)
        GPIO.output(self.pin, 0)
        time.sleep(.028)

    def sendCommand(self, compulinkCommand, compulinkaddress=None):
        if not compulinkaddress:
            compulinkaddress = self.address
        if self.debug:
            print "Sending address: " + str(self.address) + " command: " + str(compulinkCommand)
        # send address
        for x in [8, 4, 2, 1]:
            if 0 != compulinkaddress & x:
                self.pulse1()
            else:
                self.pulse0()
        # send command
        for x in [8, 4, 2, 1]:
            if 0 != compulinkCommand & x:
                self.pulse1()
            else:
                self.pulse0()
        self.pulseStop()
