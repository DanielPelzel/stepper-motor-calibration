# Stepper Motor Calibration
This tool uses PyQt5 to find out the maximum speed of a stepper motor.

## Hardware I use
- ESP32-DevKit
- TMC2209 Stepper Motor Driver
- NEMA-17 Stepper Motor

## Functionality
The speed of your motor can be adjusted with the slider. The program uses this input to calculate the demanded delay in microseconds, so your stepper reaches that speed. To work properly a bipolar stepper motor is required. Setup your driver so the motor makes 8 microsteps. Click the "Start" button to send your settings via Serial. Make sure your motor has stopped by using the "Stop" button beforehand.

## Usage 
1. Connect ESP32 via USB 
2. Flash main.cpp to ESP32
3. Run gui.py
4. Set microstepping to 8 on the driver 
5. Adjust RPM slider 
6. click start 