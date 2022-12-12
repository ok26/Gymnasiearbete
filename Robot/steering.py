import RPi.GPIO as GPIO

class Wheels:
    
    def __init__(self, rwheel, lwheel):
        self.rightForward = rwheel[0]
        self.rightBackward = rwheel[1]
        self.ENBPin = rwheel[2]
        self.leftForward = lwheel[0]
        self.leftBackward = lwheel[1]
        self.ENAPin = lwheel[2]
        
        GPIO.setup(self.rightForward, GPIO.OUT)
        GPIO.setup(self.rightBackward, GPIO.OUT)
        GPIO.setup(self.leftForward, GPIO.OUT)
        GPIO.setup(self.leftBackward, GPIO.OUT)
        GPIO.setup(self.ENAPin, GPIO.OUT)
        GPIO.setup(self.ENBPin, GPIO.OUT)
        
        self.ENA = GPIO.PWM(self.ENAPin, 60)
        self.ENB = GPIO.PWM(self.ENBPin, 60)
        self.ENA.start(0)
        self.ENB.start(0)
        self.ENADutyCycle = 0
        self.ENBDutyCycle = 0
        
    def updateENA(self, duty):
        if self.ENADutyCycle != duty:
            self.ENA.ChangeDutyCycle(duty)
            self.ENADutyCycle = duty
    
    def updateENB(self, duty):
        if self.ENBDutyCycle != duty:
            self.ENB.ChangeDutyCycle(duty)
            self.ENBDutyCycle = duty
        
    def leftTurn(self, duty):
        self.updateENB(duty)
        if not GPIO.input(self.rightForward):
            GPIO.output(self.rightForward, True)
    
    def rightTurn(self, duty):
        self.updateENA(duty)
        if not GPIO.input(self.leftForward):
            GPIO.output(self.leftForward, True)
    
    def forward(self, leftDuty, rightDuty):
        self.updateENA(leftDuty)
        self.updateENB(rightDuty)
        if not GPIO.input(self.rightForward):
            GPIO.output(self.rightForward, True)
        if not GPIO.input(self.leftForward):
            GPIO.output(self.leftForward, True)
            
    def updatePWM(self, leftDuty, rightDuty):
        self.updateENA(leftDuty)
        self.updateENB(rightDuty)
    
    def stop(self, left, right):
        if left and GPIO.input(self.leftForward):
            GPIO.output(self.leftForward, False)
        if right and GPIO.input(self.rightForward):
            GPIO.output(self.rightForward, False)
