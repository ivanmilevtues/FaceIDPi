# import RPi.GPIO as GPIO


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    channel_list = [1, 2, 3]

    GPIO.setup(channel_list, GPIO.OUT)
    GPIO.output(channel_list, GPIO.HIGH)

def release_relay():
    print("RELAY RELEASED")
    # GPIO.output(2, GPIO.LOW)


def on_end():
    GPIO.cleanup()
