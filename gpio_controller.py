import RPi.GPIO as GPIO
import sys


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    channel_list = [3, 5, 7, 11]

    GPIO.setup(channel_list, GPIO.OUT)
    GPIO.output(channel_list, GPIO.HIGH)

def release_relay():
    print("RELEASE RELAY CALLED")
    GPIO.output(5, GPIO.LOW)


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
