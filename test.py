import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Initialize I2C and PCA9685
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # MG996R expects 50 Hz

# Setup servo on channel 0 (adjust if needed)
# MG996R often benefits from extended pulse width range
my_servo = servo.Servo(pca.channels[0], min_pulse=600, max_pulse=2500)

try:
    print("Sweeping slowly from 0° to 180°")

    for angle in range(0, 181):
        my_servo.angle = angle
        print(f"Angle: {angle}°")
        time.sleep(0.15)  # 50ms per step = ~9 seconds full sweep

    print("Done sweeping.")

finally:
    pca.deinit()
    
