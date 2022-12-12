import RPi.GPIO as GPIO
from time import sleep

class Servo:
    
    def __init__(self, pwm_pin, defaultAngle=90, boundaries=[5,175]):
        GPIO.setup(pwm_pin, GPIO.OUT)
        self.pwm_pin = pwm_pin
        self.pwm = GPIO.PWM(pwm_pin, 50)
        self.pwm.start(0)
        boundaries[0] = max(0, boundaries[0])
        boundaries[1] = max(min(180, boundaries[1]), boundaries[0])
        self.boundaries = boundaries
        self.setAngle(defaultAngle)
        self.angle = defaultAngle
        
    def checkAngle(self, angle):
        return min(max(angle, self.boundaries[0]), self.boundaries[1])
    
    def calcDuty(self, angle):
        return angle / 18 + 2
        
    def setAngle(self, angle):
        angle = self.checkAngle(angle)
        duty = self.calcDuty(angle)
        self.pwm.ChangeDutyCycle(duty)
        GPIO.output(self.pwm_pin, True)
        sleep(0.15)
        GPIO.output(self.pwm_pin, False)
        self.pwm.ChangeDutyCycle(0)
        self.angle = angle
    
    def moveDeltaAngle(self, deltaAngle):
        newAngle = self.angle + deltaAngle
        newAngle = self.checkAngle(newAngle)
        duty = self.calcDuty(newAngle)
        self.pwm.ChangeDutyCycle(duty)
        self.angle = newAngle
    
    def swoop(self, targetAngle, steps):
        targetAngle = self.checkAngle(targetAngle)
        GPIO.output(self.pwm_pin, True)
        for step in range(1, steps+1):
            angle = self.angle + (targetAngle-self.angle) * step/steps
            duty = self.calcDuty(angle)
            self.pwm.ChangeDutyCycle(duty)
            sleep(0.05)
        self.angle = targetAngle
        GPIO.output(self.pwm_pin, False)
        self.pwm.ChangeDutyCycle(0)
            