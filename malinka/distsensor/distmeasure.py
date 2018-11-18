# libraries
import RPi.GPIO as GPIO
import time

# consts
PROBE_TIME = 0.5    # probe time

# set GPIO pins for HC-SR04
GPIO_TRIG = 18
GPIO_ECHO = 24

# set LEDs pins
GPIO_GREEN_LED = 21
GPIO_YELLOW_LED = 16
GPIO_RED_LED = 20

def setup():
    # GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)

    # set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIG, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    # setup LEDs (OUT)
    GPIO.setup(GPIO_GREEN_LED, GPIO.OUT)
    GPIO.setup(GPIO_YELLOW_LED, GPIO.OUT)
    GPIO.setup(GPIO_RED_LED, GPIO.OUT)

def trigger_signal():
    GPIO.output(GPIO_TRIG, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIG, False)

def distance():
    start_time = time.time()
    stop_time = time.time()
    trigger_signal()

    # save trigger time
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    # save arrival time
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # time difference
    time_diff = stop_time - start_time
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2 (there and back)
    return (time_diff * 34300) / 2

def turn_leds(dist):
    if dist >= 15:
        GPIO.output(GPIO_GREEN_LED, False)
        GPIO.output(GPIO_YELLOW_LED, False)
        GPIO.output(GPIO_RED_LED, False)
    elif dist > 10:
        GPIO.output(GPIO_GREEN_LED, True)
        GPIO.output(GPIO_YELLOW_LED, False)
        GPIO.output(GPIO_RED_LED, False)
    elif dist > 5:
        GPIO.output(GPIO_GREEN_LED, True)
        GPIO.output(GPIO_YELLOW_LED, True)
        GPIO.output(GPIO_RED_LED, False)
    else:
        GPIO.output(GPIO_GREEN_LED, True)
        GPIO.output(GPIO_YELLOW_LED, True)
        GPIO.output(GPIO_RED_LED, True)

if __name__ == '__main__':

    try:
        setup()

        while True:
            dist = distance()
            turn_leds(dist)
            print "distance = {0:6.2f}".format(dist)
            time.sleep(PROBE_TIME)

    except KeyboardInterrupt:
        print("stopped by ctrl-c")
        GPIO.cleanup()
