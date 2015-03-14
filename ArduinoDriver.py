import procgame.game 
from procgame.game.gameitems import GameItem #, AttrCollection, Driver
import serial
import logging
import time

class ArduinoClient(object):
    """ the serial bridge to the arduino board -- right now it runs in the same thread, but that's temporary """

    serial_client = None

    def __init__(self, com_port, baud_rate, timeout=1):
        self.logger = logging.getLogger('game.driver')
        try:
            self.serial_client = serial.Serial(port=com_port,baudrate=baud_rate,timeout=timeout)
            ## Need to sleep here for a couple of seconds to let the port settle down
            time.sleep(4)
            self.logger.info("Arduino/Serial device ONLINE")
        except serial.serialutil.SerialException, e:
            #raise e
            self.logger.info("Arduino/Serial device OFFLINE; check connection to %s " % com_port)
            self.serial_client = None

    def raw_write(self,servalue):
        if(self.serial_client is not None):
            self.serial_client.write(servalue)
        else:
            self.logger.info("Serial client OFFLINE - write supressed")

    def rgbschedule(self, colour, lamp_num, sched, now, repeat = True):
        self.logger.debug("SENDING %d - schedule %08x", lamp_num, sched)
        self.raw_write(colour+chr(lamp_num)+chr((sched >>24) & 255)+chr((sched >>16) & 255)+chr((sched >>8) & 255)+chr((sched) & 255))


class wsRGB(procgame.game.VirtualDriver):
    """Represents a ws2811/ws2812 based RGB LED, driven via serial communication through :class:`ArduinoClient`.
    
    Subclass of :class:`procgame.game.VirtualDriver`.

    A 'first-class' driver object for these RGB leds.  
    It leverages the fact that VirtualDriver does pretty much everything as long as you provide subclassed 
    pulse, schedule and disable methods (which are provided here).  

    Right now patter and pulsed_patter will not work because I haven't 
    coded them and virtualdriver doesn't implement them via schedule.  Shouldn't be that hard to do
    (just don't patter and pulsed_patter!!)

    You can use these in FakePinProc or real PinProc.  If the Arduino is disconnected, they just won't work.
    """
    
    color = 'W'

    def __init__(self, game, name, number, color='W'):
        super(wsRGB, self).__init__(game, name, number, polarity=True)

        if not hasattr(game,'arduino_client') or game.arduino_client is None:
            raise ValueError, 'Cannot initialize a wsRGB without an initialized arduino_client attribute in the game object'
        self.color = color

    def state(self):
        return self.state        

    def disable(self):
        """Schedules this driver to be enabled according to the given `schedule` bitmask."""
        super(wsRGB, self).disable()
        self.logger.debug("wsRGB Driver %s - disable" % self.name)
        self.game.arduino_client.rgbschedule(self.color, self.number, 0x0, True, True)

    def pulse(self, milliseconds=None):
        """Enables this driver for `milliseconds`.
        
        If no parameters are provided or `milliseconds` is `None`, :attr:`default_pulse_time` is used.
        ``ValueError`` will be raised if `milliseconds` is outside of the range 0-255.
        """
        super(wsRGB, self).pulse(milliseconds)

        self.logger.debug("sRGB Driver %s - pulse %d", self.name, milliseconds)
        # self.game.proc.driver_pulse(self.number, milliseconds)
        self.game.arduino_client.rgbschedule(self.color, self.number, milliseconds, False, repeat = False)


    def schedule(self, schedule, cycle_seconds=0, now=True):
        """Schedules this driver to be enabled according to the given `schedule` bitmask."""
        super(wsRGB, self).schedule(schedule, cycle_seconds, now)
        self.logger.debug("wsRGB Driver %s - schedule %08x" % (self.name, schedule))
        self.game.arduino_client.rgbschedule(self.color, self.number, schedule, now, repeat=True)

    def patter(self, on_time=10, off_time=10, original_on_time=0, now=True):
        """Enables a pitter-patter sequence.  

        It starts by activating the driver for `original_on_time` milliseconds.  
        Then it repeatedly turns the driver on for `on_time` milliseconds and off for 
        `off_time` milliseconds.
        """

        if not original_on_time in range(256):
            raise ValueError, 'original_on_time must be in range 0-255.'
        if not on_time in range(128):
            raise ValueError, 'on_time must be in range 0-127.'
        if not off_time in range(128):
            raise ValueError, 'off_time must be in range 0-127.'

        self.logger.debug("Driver %s - patter on:%d, off:%d, orig_on:%d, now:%s", self.name, on_time, off_time, original_on_time, now)

        sched = 0x0 + on_time
        self.game.arduino_client.rgbschedule(self.color, self.number, sched, now, repeat = True)
        self.last_time_changed = time.time()

    def pulsed_patter(self, on_time=10, off_time=10, run_time=0, now=True):
        """Enables a pitter-patter sequence that runs for `run_time` milliseconds.  

        Until it ends, the sequence repeatedly turns the driver on for `on_time` 
        milliseconds and off for `off_time` milliseconds.
        """

        if not run_time in range(256):
            raise ValueError, 'run_time must be in range 0-255.'
        if not on_time in range(128):
            raise ValueError, 'on_time must be in range 0-127.'
        if not off_time in range(128):
            raise ValueError, 'off_time must be in range 0-127.'

        self.logger.debug("Driver %s - pulsed patter on:%d, off:%d, run_time:%d, now:%s", self.name, on_time, off_time, run_time, now)

        time = on_time + off_time
        sched = 0x0 + on_time
        # figure out how many time intervales there are in 255
        # add an ontime shifted by time repeatedly
        raise ValueError, "Lazy Programmer: pulsed_patter is not supported in these LEDs yet."
        self.game.arduino_client.rgbschedule(self.color, self.number, sched, now, repeat = True)

        # self.game.proc.driver_pulsed_patter(self.number, on_time, off_time, run_time, now)
        self.last_time_changed = time.time()


