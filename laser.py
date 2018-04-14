import RPi.GPIO as GPIO
import time
import lcddriver

# detect if sensor state has changed
def check_sensor(gpio_id, state):
    input = GPIO.input(gpio_id)

    if state != input:
        print("Detected toggle on channel {}: {}".format(gpio_id, input))
    return input

# sensor1 is at the entrance
# sensor2 is in the floor
sensor1 = 23
sensor2 = 24

# initialize screen
lcd = lcddriver.lcd()
lcd.lcd_clear()

# initialize GPIO including sensors
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor1, GPIO.IN)
GPIO.setup(sensor2, GPIO.IN)

# set idle sensor states to 0 (== laser on)
state_sensor1 = 0
state_sensor2 = 0

# no magic, just updating sensor states
def update_sensors():
    global state_sensor1
    global state_sensor2
    state_sensor1 = check_sensor(sensor1, state_sensor1)
    state_sensor2 = check_sensor(sensor2, state_sensor2)

# initialize amount of people in the room to 0 and display it to the screen
in_people = 0
lcd.lcd_display_string("Visitors:", 1)
lcd.lcd_display_string(str(in_people), 2)

'''actual algorithm: Infinte loop that requests the current sensor states in
order to update "in_people"'''
while True:
    update_sensors()
    # case: Someone enters
    while state_sensor1 == 1:
        update_sensors()
        if state_sensor1 == 0 and state_sensor2 == 1:
            in_people += 1
            print("This many people are in the room:", in_people)
            lcd.lcd_clear()
            lcd.lcd_display_string("Visitors:", 1)
            lcd.lcd_display_string(str(in_people), 2)
            # require sensor states to change to idle mode before continuing
            while not (state_sensor1 == 0 and state_sensor2 == 0):
                update_sensors()
    # case: Someone leaves
    while state_sensor2 == 1:
        update_sensors()
        if state_sensor1 == 1 and state_sensor2 == 0:
            # ensure that amount of people cannot be negative
            if in_people > 0:
                in_people -= 1
                print("This many people are in the room:", in_people)
                lcd.lcd_clear()
                lcd.lcd_display_string("Visitors:", 1)
                lcd.lcd_display_string(str(in_people), 2)
            # require sensor states to change to idle mode before continuing
            while not (state_sensor1 == 0 and state_sensor2 == 0):
                update_sensors()
