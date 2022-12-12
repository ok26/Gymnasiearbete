import cv2
import RPi.GPIO as GPIO

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 352)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
