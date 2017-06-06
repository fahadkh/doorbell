from picamera import PiCamera
from time import sleep
import requests
import RPi.GPIO as GPIO

# Make variables for GPIO pins
DOORBELL_GPIO = 4
GREEN_GPIO = 17
YELLOW_GPIO = 18
RED_GPIO = 27

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DOORBELL_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(GREEN_GPIO, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(YELLOW_GPIO, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(RED_GPIO, GPIO.OUT, initial=GPIO.LOW)
    GPIO.add_event_detect(DOORBELL_GPIO, GPIO.RISING)
    GPIO.add_event_callback(DOORBELL_GPIO, doorbell_pressed)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print "Ctrl+C pressed"
    except:
        print "Other error occurred"
    finally:
        GPIO.cleanup()


def doorbell_pressed(self):
    
    for i in range(0, 10):
        if GPIO.input(DOORBELL_GPIO):
            continue
        else:
            return
    picture_mode = False 
    print "Doorbell pressed!"
    filepath = '/home/pi/iot/images/test.jpg'
    url = 'http://13.58.38.35/detect'
    retry_limit = 3
    retries = 0
    success = False

    while (not success and retries < retry_limit):
        GPIO.output(YELLOW_GPIO, 1)
        sleep(.1)
        GPIO.output(YELLOW_GPIO, 0)

        if picture_mode:
            capture_image(filepath)
            break

        capture_image(filepath)
        file = open(filepath, 'rb')

        data = file.read()
        headers = {'Content-Type' : 'image/bin'}
        request = requests.post(url, data=data, headers=headers)

        file.close()

        print request.text
        if "access=true" in request.text:
            success = True
        else:
            retries += 1

    if success:
        open_lock()
    else:
        deny_access()




# Capture image from camera and write it to the file in path
def capture_image(path):
    camera = PiCamera()
    camera.start_preview()
    sleep(.3)
    camera.capture(path)
    camera.stop_preview()
    camera.close()


# Open lock using GPIO pins if access is granted
def open_lock():
    GPIO.output(GREEN_GPIO, 1)
    sleep(2)
    GPIO.output(GREEN_GPIO, 0)
    print "Opening lock"


# Deny access (perhaps flash an LED to notify user?)
def deny_access():
    GPIO.output(RED_GPIO, 1)
    sleep(0.1)
    GPIO.output(RED_GPIO, 0)
    sleep(0.1)
    GPIO.output(RED_GPIO, 1)
    sleep(0.1)
    GPIO.output(RED_GPIO, 0)
    sleep(0.1)
    GPIO.output(RED_GPIO, 1)
    sleep(0.1)
    GPIO.output(RED_GPIO, 0)
    print "Access denied"

main()
