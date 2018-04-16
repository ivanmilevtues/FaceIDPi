import RPi.GPIO as GPIO
import sys


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    channel_list = [2, 3, 4, 17]

    GPIO.setup(channel_list, GPIO.OUT)
    GPIO.output(channel_list, GPIO.HIGH)

def release_relay():
    GPIO.output(2, GPIO.LOW)


def on_end():
    GPIO.cleanup()


if __name__ == "__main__":
    arg = int(sys.argv[1])
    if arg == 1:
        setup()
    if arg == 0:
        release_relay()
    if arg == -1:
        on_end()