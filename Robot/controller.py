from microbit import *
import radio

radio.on()

def assembleMessage(speed, left_is_moving, right_is_moving, should_flip):
    """Create the message to be received by the robot"""
    UNIQUE_SIGNATURE = "DLZ"
    return UNIQUE_SIGNATURE + "/" + speed + "/" + left_is_moving + "/" + right_is_moving + "/" + should_flip


# Event Loop
while True:
    # Determine direction (either forwards or backwards)
    if accelerometer.get_y() < 300:
        display.show(Image.ARROW_N)
        speed = "100"
    else:
        display.show(Image.ARROW_S)
        speed = "-100"
    
    # Determine which wheels should turn
    if button_a.is_pressed():
        left_is_moving = "1"
    else:
        left_is_moving = "0"

    if button_b.is_pressed():
        right_is_moving = "1"
    else:
        right_is_moving = "0"

    # Determine if the flipper should be activated
    x_orientation = accelerometer.get_x()
    if x_orientation > 700 or x_orientation < -700:
        display.show(Image.SKULL)
        should_flip = "1"
    else:
        should_flip = "0"

    radioMessage = assembleMessage(speed, left_is_moving, right_is_moving, should_flip)
    radio.send(radioMessage)

    sleep(40)