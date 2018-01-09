from microbit import *
import radio

radio.on()

def assembleMessage(dir, r_speed, l_speed):
    """Create the message to be received by the robot"""
    unique_signature = "DLZ"
    return unique_signature + "/" + dir + "/" + r_speed + "/" + l_speed


# Event Loop
while True:
    y_orientation = accelerometer.get_y()

    # Determine direction (either forwards or backwards)
    if y_orientation < 300:
        display.show(Image.ARROW_N)
        direction = "forward"
    else:
        display.show(Image.ARROW_S)
        direction = "backward"
    
    # Determine which wheels should turn
    if button_a.is_pressed():
        leftSpeed = "moving"
    else:
        leftSpeed = "still"

    if button_b.is_pressed():
        rightSpeed = "moving"
    else:
        rightSpeed = "still"

    radioMessage = assembleMessage(direction, rightSpeed, leftSpeed)
    radio.send(radioMessage)

    sleep(50)