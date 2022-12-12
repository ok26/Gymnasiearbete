import cv2
import numpy as np
from time import sleep
import RPi.GPIO as GPIO
from Robot import cap
from Robot.servo import Servo
from Robot.camera import find_centroid
from Robot.steering import Wheels

def loop():
    try:
        servoX = Servo(18)
        servoY = Servo(11, defaultAngle=120, boundaries=[80,160])
        wheels = Wheels((31,33,40),(35,37,29))
        sleep(1)
        GPIO.output(servoX.pwm_pin, True)
        GPIO.output(servoY.pwm_pin, True)
        GPIO.output(wheels.rightForward, True)
        GPIO.output(wheels.leftForward, True)
        while True:
            cX, cY = find_centroid()
            if cX==-1:
                break
            if 0.43<=cX<=0.57:
                servoX.pwm.ChangeDutyCycle(0)
            else:
                deltaAngle = 0.5 * 2.72**(7 * abs(0.5-cX))
                if cX < 0.5: deltaAngle = -deltaAngle
                servoX.moveDeltaAngle(deltaAngle)
            if 0.43<=cY<=0.57:
                servoY.pwm.ChangeDutyCycle(0)
            else:
                deltaAngle = 0.5 * 2.72**(6 * abs(0.5-cY))
                if cY < 0.5: deltaAngle = -deltaAngle
                servoY.moveDeltaAngle(deltaAngle)
            
            if cX==0.5 and cY==0.5:
                wheels.updatePWM(0,0)
                #wheels.stop(True, True)
            
            else:
                right = False
                left = False
                forward = False
                rightENB = 0
                leftENA = 0
                if servoX.angle > 98:
                    rightENB = 20*2.72**(0.015*(servoX.angle-110))
                    left = True
                elif servoX.angle < 82:
                    leftENA = 20*2.72**(0.015*(70-servoX.angle))
                    right = True
                if servoY.angle > 150:
                    servoY.setAngle(120)
                    servoX.setAngle(90)
                    continue
                elif servoY.angle > 100:
                    if right:
                        rightENB = 30*2.72**(0.02*(servoY.angle-100))
                        leftENA = 30+rightENB
                    elif left:
                        leftENA = 30*2.72**(0.02*(servoY.angle-100))
                        rightENB = 30+leftENA
                    else:
                        leftENA = rightENB = 30*2.72**(0.02*(servoY.angle-100))
                    forward = True
                wheels.updatePWM(leftENA, rightENB)
                
            
    except Exception as err:
        print(err)
        
    cap.release()
    cv2.destroyAllWindows()
    
    wheels.stop(True, True)
    wheels.ENA.stop()
    wheels.ENB.stop()
    
    servoX.setAngle(90)
    servoY.setAngle(120)
    sleep(1)
    servoX.setAngle(90)
    servoY.setAngle(120)
    servoX.pwm.stop()
    servoY.pwm.stop()
    
    GPIO.output(servoX.pwm_pin, False)
    GPIO.output(servoY.pwm_pin, False)
    GPIO.output(wheels.rightForward, False)
    GPIO.output(wheels.leftForward, False)
    GPIO.cleanup()
    
    
    