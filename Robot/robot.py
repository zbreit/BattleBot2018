from microbit import *
import radio

radio.on()

# Motobit classes sourced from Github: https://github.com/hsshss/motobit-micropython
class MotoBitMotor:
    FORWARD_FLAG = 0x80

    def __init__(self, i2c_addr, cmd_speed, invert):
        self.i2c_addr = i2c_addr
        self.cmd_speed = cmd_speed
        self.invert = invert

    def __drive(self, speed):
        flags = 0
        if self.invert:
            speed = -speed
        if speed >= 0:
            flags |= MotoBitMotor.FORWARD_FLAG
        speed = int(speed / 100 * 127)
        if speed < -127:
            speed = -127
        if speed > 127:
            speed = 127
        speed = (speed & 0x7f) | flags
        i2c.write(self.i2c_addr, bytes([self.cmd_speed, speed]))

    def forward(self, speed):
        '''Forward motor control.
        Args:
            speed (int|float): -100 ~ +100
        '''
        self.__drive(speed)

    def reverse(self, speed):
        '''Reverse motor control.
        Args:
            speed (int|float): -100 ~ +100
        '''
        self.__drive(-speed)
class MotoBit:
    I2C_ADDR = 0x59
    CMD_ENABLE = 0x70
    CMD_SPEED_LEFT = 0x21
    CMD_SPEED_RIGHT = 0x20

    def enable(self):
        '''Enable motor driver.
        '''
        i2c.write(MotoBit.I2C_ADDR, bytes([MotoBit.CMD_ENABLE, 0x01]))

    def disable(self):
        '''Disable motor driver.
        '''
        i2c.write(MotoBit.I2C_ADDR, bytes([MotoBit.CMD_ENABLE, 0x00]))

    def left_motor(self, invert = False):
        '''Acquire left motor object.
        Args:
            invert (bool): Invert polarity. (default: False)
        '''
        return MotoBitMotor(MotoBit.I2C_ADDR, MotoBit.CMD_SPEED_LEFT, invert)

    def right_motor(self, invert = False):
        '''Acquire right motor object.
        Args:
            invert (bool): Invert polarity. (default: False)
        '''
        return MotoBitMotor(MotoBit.I2C_ADDR, MotoBit.CMD_SPEED_RIGHT, invert)

# Enable motor driver
motobit = MotoBit()
motobit.enable() 

# Declare motors
leftMotor = motobit.left_motor(invert = True)
rightMotor = motobit.right_motor(invert = True)

# Couldn't get the servo library to work properly, 
# so we were unable to test the flipper's functionality
# flipperMotor = Servo(pin15)


def parse(message):
    """Returns a 4 element list that contains info from the controller"""
    return list(map(int, remove_signature(message)))

def is_signed_message(message):
    """Returns true if the message contains our unique signature"""
    UNIQUE_SIGNATURE = "DLZ"
    
    if message[0] == UNIQUE_SIGNATURE:
        return True
    else:
        return False

def remove_signature(message):
    """Remove the 3 Letter signature and the '/' found at the beginning of a valid message"""
    return message[1:]

def tank_drive(speed, left_is_moving, right_is_moving):
    """ Drives the robot in tank drive. Direction indicates whether the robot will drive forwards or backwards"""

    if right_is_moving:
        rightMotor.forward(speed)
    else:
        rightMotor.forward(0)

    if left_is_moving:
        leftMotor.forward(speed)
    else:
        leftMotor.forward(0)

    display_if_moving(left_is_moving, right_is_moving)

def display_if_moving(left, right):
    """Uses the micro:bit's display to show whether the robot is moving or not"""
    if left or right:
        display.show(Image.HAPPY)
    else:
        display.show(Image.SAD)

# Event Loop
while True:
    incoming = radio.receive()

    # Assert that the message is not 'NoneType'
    if not incoming:
        display.show(Image.SKULL)
        sleep(50)
        continue
    else:
        incoming = incoming.split("/")

    if is_signed_message(incoming):
        direction_list   = parse(incoming)
        speed           = direction_list[0]
        left_is_moving  = direction_list[1]
        right_is_moving = direction_list[2]
        should_flip     = direction_list[3]
        tank_drive(speed, left_is_moving, right_is_moving)
        if should_flip:
            display.show(Image.SKULL)

    sleep(40)