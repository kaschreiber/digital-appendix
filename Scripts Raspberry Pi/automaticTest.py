# Automatic test script for multiple servos
import time
import busio
from board import SDA, SCL
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# I2C-connection for servo control
i2c = busio.I2C(SCL, SDA)

# PCA9685 initialization
pca = PCA9685(i2c)
pca.frequency = 50  # Standard frequency for servos

# (1, 3, 5, 7, 8, 9, 11, 13 or 15)
# Eye 1
servo_1 = servo.Servo(pca.channels[0])  # up and down
servo_2 = servo.Servo(pca.channels[2])  # open and close
servo_3 = servo.Servo(pca.channels[4])  # left and right
# Eye 2
servo_4 = servo.Servo(pca.channels[6])  # up and down
servo_5 = servo.Servo(pca.channels[7])  # open and close
servo_6 = servo.Servo(pca.channels[8])  # left and right
# Eye 3
servo_7 = servo.Servo(pca.channels[10])  # up and down
servo_8 = servo.Servo(pca.channels[12])  # open and close
servo_9 = servo.Servo(pca.channels[14])  # left and right

servo_1.angle = 90  # start position for Servo 1
servo_4.angle = 90  # start position for Servo 4
servo_7.angle = 90  # start position for Servo 7
time.sleep(1)
servo_2.angle = 90  # start position for Servo 2
servo_5.angle = 90  # start position for Servo 5
servo_8.angle = 90  # start position for Servo 8
time.sleep(1)
servo_3.angle = 90  # start position for Servo 3
servo_6.angle = 90  # start position for Servo 6
servo_9.angle = 90  # start position for Servo 9
time.sleep(1)

# Movement test
print("Starting test of all three servos...")

servo_2.angle = 180
servo_5.angle = 180
servo_8.angle = 180
time.sleep(1)
servo_2.angle = 0
servo_5.angle = 0
servo_8.angle = 0
time.sleep(1)

servo_3.angle = 20
servo_6.angle = 20
servo_9.angle = 20
time.sleep(1)
servo_1.angle = 0
servo_4.angle = 0
servo_7.angle = 0
time.sleep(1)

servo_2.angle = 180
servo_5.angle = 180
servo_8.angle = 180
time.sleep(1)
servo_2.angle = 0
servo_5.angle = 0
servo_8.angle = 0
time.sleep(1)

servo_3.angle = 180
servo_6.angle = 180
servo_9.angle = 180
time.sleep(1)
servo_1.angle = 180
servo_4.angle = 180
servo_7.angle = 180
time.sleep(1)

servo_2.angle = 180
servo_5.angle = 180
servo_8.angle = 180
time.sleep(1)
servo_2.angle = 0
servo_5.angle = 0
servo_8.angle = 0
time.sleep(1)

servo_3.angle = 90
servo_6.angle = 90
servo_9.angle = 90
time.sleep(1)   
servo_1.angle = 90
servo_4.angle = 90
servo_7.angle = 90
time.sleep(1)   
servo_2.angle = 90
servo_5.angle = 90
servo_8.angle = 90
time.sleep(1)

print("Test completed. All servos returned to center position (90°).")
