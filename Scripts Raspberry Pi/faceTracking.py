# Main script for face tracking and servo control using Raspberry Pi camera and PCA9685
import cv2
import math
from picamera2 import Picamera2
from cvzone.FaceDetectionModule import FaceDetector
import time
import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

WIDTH = 640
HEIGHT = 480

# Initialize face detector from cvzone
detector = FaceDetector(minDetectionCon=0.75)

# Code Raspberry Pi camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (WIDTH, HEIGHT)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

# I2C-connection for servo control
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50

# Eye 1
previous_angle_01 = 90 
previous_angle_02 = 90 
previous_angle_03 = 90
# Eye 2
previous_angle_04 = 90
previous_angle_05 = 90
previous_angle_06 = 90
# Eye 3
previous_angle_07 = 90
previous_angle_08 = 90
previous_angle_09 = 90
alpha = 0.2          # Smoothing factor (between 0 and 1)

MIN_SERVO_REST = 0
MIN_SERVO_03_06_09 = 20
LID_OPEN = 40

MAX_SERVO = 180
LID_CLOSE = 180

# Eye 1
my_servo_01 = servo.Servo(pca.channels[0]) # up and down
my_servo_02 = servo.Servo(pca.channels[2]) # lid movement
my_servo_03 = servo.Servo(pca.channels[4]) # left and right

# Eye 2
my_servo_04 = servo.Servo(pca.channels[6]) # up and down
my_servo_05 = servo.Servo(pca.channels[7]) # lid movement
my_servo_06 = servo.Servo(pca.channels[8]) # left and right

# Eye 3
my_servo_07 = servo.Servo(pca.channels[10]) # up and down
my_servo_08 = servo.Servo(pca.channels[12]) # lid movement
my_servo_09 = servo.Servo(pca.channels[14]) # left and right

my_servo_01.angle = previous_angle_01
my_servo_02.angle = previous_angle_02
my_servo_03.angle = previous_angle_03

my_servo_04.angle = previous_angle_04
my_servo_05.angle = previous_angle_05
my_servo_06.angle = previous_angle_06

my_servo_07.angle = previous_angle_07
my_servo_08.angle = previous_angle_08
my_servo_09.angle = previous_angle_09
time.sleep(0.3)  # Wait for servos to initialize
my_servo_02.angle = LID_OPEN
my_servo_05.angle = LID_OPEN
my_servo_08.angle = LID_OPEN

# Time tracking for blinking
last_blink_time = time.time()
blink_interval = 5      # Time between blinks in seconds
blink_duration = 0.5   # Duration for which the eyes remain closed in seconds

def remove_close_faces_keep_best(bboxs, min_distance=80):
    # Remove close bounding boxes by keeping the one with the highest confidence score.
    kept = []

    for b in bboxs:
        cx, cy = b['center']
        score = b['score'][0]
        keep = True

        # Compare against already kept boxes
        for i, existing in enumerate(kept):
            ecx, ecy = existing['center']
            distance = math.hypot(ecx - cx, ecy - cy)

            if distance < min_distance:
                existing_score = existing['score'][0]
                if score > existing_score:
                    kept[i] = b  # Replace with better one
                keep = False
                break

        if keep:
            kept.append(b)

    return kept

try:
    while True:
        img = picam2.capture_array()
        img, bboxs = detector.findFaces(img, draw=False)

        if bboxs:
            bboxs = remove_close_faces_keep_best(bboxs, min_distance=80)

        if bboxs:
            bbox = bboxs[0]
            x, y, w, h = bbox['bbox']
            cx, cy = bbox['center']
            score = bbox['score'][0]

            # map face position to servo angles
            raw_angle_03 = int(((WIDTH - cx) / WIDTH) * (MAX_SERVO - MIN_SERVO_03_06_09) + MIN_SERVO_03_06_09)
            raw_angle_01 = int(((HEIGHT - cy) / HEIGHT) * (MAX_SERVO - MIN_SERVO_REST) + MIN_SERVO_REST)

            # Smoothing
            smoothed_angle_03 = int(alpha * raw_angle_03 + (1 - alpha) * previous_angle_03)
            previous_angle_03 = smoothed_angle_03

            smoothed_angle_01 = int(alpha * raw_angle_01 + (1 - alpha) * previous_angle_01)
            previous_angle_01 = smoothed_angle_01

            # Movement
            my_servo_01.angle = smoothed_angle_01
            my_servo_03.angle = smoothed_angle_03

            my_servo_04.angle = smoothed_angle_01
            my_servo_06.angle = smoothed_angle_03

            my_servo_07.angle = smoothed_angle_01
            my_servo_09.angle = smoothed_angle_03

        # Time-based blinking
        current_time = time.time()

        if current_time - last_blink_time >= blink_interval:
            # Close eyes
            my_servo_02.angle = LID_CLOSE
            my_servo_05.angle = LID_CLOSE
            my_servo_08.angle = LID_CLOSE
            time.sleep(blink_duration)
            # Open eyes
            my_servo_02.angle = LID_OPEN
            my_servo_05.angle = LID_OPEN
            my_servo_08.angle = LID_OPEN
            last_blink_time = current_time

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.05)
finally:
    # Reset servos to center position
    my_servo_01.angle = 90
    my_servo_02.angle = 90
    my_servo_03.angle = 90
    my_servo_04.angle = 90
    my_servo_05.angle = 90
    my_servo_06.angle = 90
    my_servo_07.angle = 90
    my_servo_08.angle = 90
    my_servo_09.angle = 90
    time.sleep(0.3)
    pca.deinit()
    print("Programm beendet.")
