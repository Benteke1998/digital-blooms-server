This server.py controls a servo motor (via Raspberry Pi and PCA9685) to visualize screen use during family time. The flower moves (wilts/blooms) in real time based on screen time data received from your custom Android app.

Purpose
- Receives screen usage data via HTTP POST from the companion Android app.
- Translates phone activity into visible flower movement, using a servo motor.
- Part of the Social Blooms master's thesis for materializing digital behavior in the home.

Included in this repository is two servo scripts that was used for testing. One will make the servo go from 0-180 degrees and the other will rotate the servo back to 0 degrees.
