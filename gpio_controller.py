import RPi.GPIO as GPIO
import sys
from time import sleep


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    channel_list = [3, 5, 7, 11]
    channel_in = [13]

    GPIO.setup(channel_list, GPIO.OUT)
    GPIO.setup(channel_in, GPIO.IN)
    GPIO.output(channel_list, GPIO.HIGH)


def release_relay():
    print("REALY Release")
    GPIO.output(5, GPIO.LOW)
    sleep(5)
    GPIO.output(5, GPIO.HIGH)


def on_end():
    GPIO.cleanup()


def read_btn():
    exit(int(GPIO.input(13)))

if __name__ == "__main__":
    arg = int(sys.argv[1])
    if arg == 0:
        setup()
        release_relay()
    if arg == -1:
        on_end()
    if arg == 1:
        read_btn()
