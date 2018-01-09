from microbit import *
import radio

# Servo class sourced from Github
# TODO: Find actual link
class Servo:

    """
    A simple class for controlling hobby servos.
    Args:
        pin (pin0 .. pin3): The pin where servo is connected.
        freq (int): The frequency of the signal, in hertz.
        min_us (int): The minimum signal length supported by the servo.
        max_us (int): The maximum signal length supported by the servo.
        angle (int): The angle between minimum and maximum positions.
    Usage:
        SG90 @ 3.3v servo connected to pin0
        = Servo(pin0).write_angle(90)
    """

    def __init__(self, pin, freq=50, min_us=600, max_us=2400, angle=180):
        self.min_us = min_us
        self.max_us = max_us
        self.us = 0
        self.freq = freq
        self.angle = angle
        self.analog_period = 0
        self.pin = pin
        analog_period = round((1/self.freq) * 1000)  # hertz to miliseconds
        self.pin.set_analog_period(analog_period)

    def write_us(self, us):
        us = min(self.max_us, max(self.min_us, us))
        duty = round(us * 1024 * self.freq // 1000000)
        self.pin.write_analog(duty)
        self.pin.write_digital(0)  # turn the pin off

    def write_angle(self, degrees=None):
        degrees = degrees % 360
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * degrees // self.angle
        self.write_us(us)

radio.on()

# Global Constants
leftMotor = Servo(pin15)
rightMotor = Servo(pin16)

def parse(message):
    """Returns a 3 element list that contains info from the controller"""
    return remove_signature(message).split('/')

def is_signed_message(message):
    """Returns true if the message contains our unique signature"""
    UNIQUE_SIGNATURE = "DLZ"
    # Assert that the message is not 'NoneType'
    if not message:
        return False
    
    if message[0:3] == UNIQUE_SIGNATURE:
        return True
    else:
        return False

def remove_signature(message):
    """Remove the 3 Letter signature and the '/' found at the beginning of a valid message"""
    return message[4:]

def tank_drive(direction, lSpeed, rSpeed):
    """ Drives the robot in tank drive. Direction indicates whether the robot will drive forwards or backwards"""
    angles = {
        "forward": 0,
        "backward": 180
    }

    speed = angles[direction]

    if rSpeed == "moving":
        rightMotor.write_angle(speed)
    elif rSpeed == "still":
        rightMotor.write_angle(90)

    if lSpeed == "moving":
        leftMotor.write_angle(180 - speed)
    elif lSpeed == "still":
        leftMotor.write_angle(90)

# Event Loop
while True:
    incoming = radio.receive()
    if is_signed_message(incoming):
        directionList = parse(incoming)
    else:
        directionList = []
    # This is totally secure
    if len(directionList) == 3:
        direction = directionList[0]
        rSpeed    = directionList[1]
        lSpeed    = directionList[2]
        tank_drive(direction, lSpeed, rSpeed)

    sleep(50)