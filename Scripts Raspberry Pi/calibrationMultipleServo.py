# This script is used to calibrate multiple servo motors connected to a PCA9685 PWM driver.
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

# Movement test
print("Starting test of all three servos...")

while True:
    # get console input for servo angles and servo number
    try:
        servo_number = int(input("Enter the servo number (1, 2, 3, 4, 5, 6, 7, 8 or 9): "))
        angle = int(input("Enter the angle (0-180): "))

        if servo_number == 1:
            angle = max(0, min(180, angle))
            servo_1.angle = angle
            print(f"Servo 1 set to {angle} degrees.")
        elif servo_number == 2:
            angle = max(0, min(180, angle))
            servo_2.angle = angle
            print(f"Servo 2 set to {angle} degrees.")
        elif servo_number == 3:
            angle = max(0, min(180, angle))
            servo_3.angle = angle
            print(f"Servo 3 set to {angle} degrees.")
        elif servo_number == 4:
            angle = max(0, min(180, angle))
            servo_4.angle = angle
            print(f"Servo 4 set to {angle} degrees.")
        elif servo_number == 5:
            angle = max(0, min(180, angle))
            servo_5.angle = angle
            print(f"Servo 5 set to {angle} degrees.")
        elif servo_number == 6:
            angle = max(0, min(180, angle))
            servo_6.angle = angle
            print(f"Servo 6 set to {angle} degrees.")
        elif servo_number == 7:
            angle = max(0, min(180, angle))
            servo_7.angle = angle
            print(f"Servo 7 set to {angle} degrees.")
        elif servo_number == 8:
            angle = max(0, min(180, angle))
            servo_8.angle = angle
            print(f"Servo 8 set to {angle} degrees.")
        elif servo_number == 9:
            angle = max(0, min(180, angle))
            servo_9.angle = angle
            print(f"Servo 9 set to {angle} degrees.")
        else:
            print("Test aborted. Invalid servo number.")
            break

        time.sleep(1)  # Short pause to see the movement
    except ValueError:
        print("Invalid input. Please enter a number.")
    except KeyboardInterrupt:
        print("\nTest aborted.")
        break
# Move all servos back to center
print("Moving all servos back to center...")
servo_1.angle = 90
time.sleep(1)
servo_2.angle = 90
time.sleep(1)
servo_3.angle = 90
time.sleep(1)
servo_4.angle = 90
time.sleep(1)
servo_5.angle = 90
time.sleep(1)
servo_6.angle = 90
time.sleep(1)
servo_7.angle = 90
time.sleep(1)
servo_8.angle = 90
time.sleep(1)
servo_9.angle = 90
time.sleep(1)