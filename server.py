import RPi.GPIO as GPIO
import itertools
import time

GPIO.setmode(GPIO.BCM)

CAMERA_SERVO_PIN = 18
GPIO.setup(CAMERA_SERVO_PIN, GPIO.OUT)
camera_servo = GPIO.PWM(CAMERA_SERVO_PIN, 50)
camera_servo.start(0)

PINS = [[17, 27, 23, 24], [5, 6, 26, 16]]
GPIO.setup(list(itertools.chain(*PINS)), GPIO.OUT)
motors = [[GPIO.PWM(pins, 100) for pins in motor] for motor in PINS]
for motor in motors:
    for pin in motor:
        pin.start(0)


def reset():
    # GPIO.output(list(itertools.chain(*PINS)), GPIO.LOW)
    for motor in itertools.chain(*motors):
        # motor.stop()
        motor.ChangeDutyCycle(0)


def move(direction, speed):
    DIRECTIONS = {
        "forward": [(0, 1), (0, 3), (1, 1), (1, 3)],
        "backward": [(0, 0), (0, 2), (1, 0), (1, 2)],
        "left": [(0, 1), (0, 3), (1, 0), (1, 2)],
        "right": [(0, 0), (0, 2), (1, 1), (1, 3)],
        "stop": []
    }

    assert direction in DIRECTIONS, "Invalid direction"
    assert 0 <= speed <= 100, "Invalid speed"

    reset()

    for mid, motor in enumerate(motors):
        for pid, pin in enumerate(motor):
            if (mid, pid) in DIRECTIONS[direction]:
                # pin.start(speed)
                pin.ChangeDutyCycle(speed)
            else:
                # pin.stop()
                pin.ChangeDutyCycle(0)


def set_camera_angle(angle):
    assert 0 <= angle <= 180, "Invalid angle"

    camera_servo.ChangeDutyCycle(angle / 180 * 11 + 1)
    time.sleep(0.1)
    camera_servo.ChangeDutyCycle(0)
