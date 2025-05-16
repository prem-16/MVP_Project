import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
p = GPIO.PWM(12, 100)
p.start(5)
time.sleep(5)
p.stop()
GPIO.cleanup()
