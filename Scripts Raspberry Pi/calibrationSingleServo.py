# This script is used to calibrate a single servo motor connected to a PCA9685 PWM driver.
import time
import busio
from board import SDA, SCL
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# I2C-connection for servo control
i2c = busio.I2C(SCL, SDA)

# Initialize PCA9685 for servo control
pca = PCA9685(i2c)
pca.frequency = 50  # Standard frequency for servos

print("Starting test of a servo...")

# Select servo
while True:
    try:
        servo_number = int(input("Enter the servo number (1, 3, 5, 7, 8, 9, 11, 13 or 15): "))
        if servo_number not in [1, 3, 5, 7, 8, 9, 11, 13, 15]:
            print("Only 1, 3, 5, 7, 8, 9, 11, 13 or 15 allowed.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a number.")

# Initialize servo (Index = Number - 1) and set to initial position
my_servo = servo.Servo(pca.channels[servo_number - 1])
angle = 90
my_servo.angle = angle
print(f"Servo {servo_number} set to initial position {angle}°.")

try:
    while True:
        try:
            angle = int(input("Enter the angle (0-180) (or -1 to quit): "))
            if angle == -1:
                break
            angle = max(0, min(180, angle))  # Clamp angle between 0 and 180
            my_servo.angle = angle
            print(f"Servo {servo_number} moved to {angle}°")
            time.sleep(0.5)
        except ValueError:
            print("Invalid input. Please enter a number.")
except KeyboardInterrupt:
    print("\nAborted by user.")

# Move back to center
print("Moving servo back to center...")
my_servo.angle = 90
time.sleep(0.5)
print("Done. Servo is at 90°, PWM disabled.")
