import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Initialize I2C and PCA9685
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # 50Hz for MG996R

# Setup servo on channel 0 with custom pulse range
my_servo = servo.Servo(pca.channels[0], min_pulse=600, max_pulse=2500)

try:
    print("Setting servo to 0°")
    my_servo.angle = 0
    time.sleep(1)  # Give it a moment to reach position
finally:
    pca.deinit()
    print("PCA9685 deinitialized")
