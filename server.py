from flask import Flask, request, jsonify
import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

app = Flask(__name__)

# Initialize I2C and PCA9685
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50

# Initialize servo on channel 0
my_servo = servo.Servo(pca.channels[0])

# State variables
servo_angle = 0
prev_screen_on_time = 0
continuous_usage_count = 0
inactivity_count = 0

def move_servo_to(target_angle):
    """Move servo to target_angle smoothly, with range clamping."""
    global servo_angle
    target_angle = max(0, min(180, target_angle))
    step = 1 if target_angle > servo_angle else -1
    for angle in range(servo_angle, target_angle + step, step):
        my_servo.angle = angle
        print(f"Servo angle: {angle}")
        time.sleep(0.1)
    servo_angle = target_angle

@app.route('/data', methods=['POST'])
def update_usage():
    global servo_angle, prev_screen_on_time, continuous_usage_count, inactivity_count

    data = request.get_json()
    print(f"Incoming JSON: {data}")

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    # 1. Handle unlock event FIRST
    if 'event' in data and data['event'] == 'unlock':
        print("Phone unlock detected. Rotating +2°.")
        move_servo_to(min(servo_angle + 2, 180))
        return jsonify({"status": "unlock event processed"}), 200

    # 2. Handle reset signal (all zeros)
try:
    session_duration = int(data.get('session_duration', 0))
    session_delta = int(data.get('session_delta', 0))
    screen_on_time = int(data.get('screen_on_time', 0))
    screen_delta = int(data.get('screen_delta', 0))
except (ValueError, TypeError):
    return jsonify({"error": "Invalid data format"}), 400

# Trigger reset ONLY if ALL are explicitly zero AND not None
    if session_duration == 0 and session_delta == 0 and screen_on_time == 0 and screen_delta == 0:
        print("Reset signal received. Moving servo to 0°.")
        move_servo_to(0)
        servo_angle = 0
        prev_screen_on_time = 0
        continuous_usage_count = 0
        inactivity_count = 0
        return jsonify({"status": "reset done"}), 200

    # --- 3. Track continuous screen usage (screen_delta > 0) ---
    if screen_delta == session_delta:
        continuous_usage_count += 1
        print(f"Continuous usage count: {continuous_usage_count}")
    else:
        continuous_usage_count = 0

    if continuous_usage_count >= 3:  # 3 x 10s = 30s continuous use
        print("30s continuous use detected. Rotating +5°.")
        move_servo_to(min(servo_angle + 5, 180))
        continuous_usage_count = 0

    # --- 4. Track inactivity (screen_delta == 0) ---
    if screen_delta == 0:
        inactivity_count += 1
        print(f"Inactivity count: {inactivity_count}")
    else:
        inactivity_count = 0

    if inactivity_count >= 18:  # 18 x 10s = 3 min inactivity
        print("3 min inactivity detected. Rotating -5°.")
        move_servo_to(max(servo_angle - 5, 0))
        inactivity_count = 0

    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

