import sys
import math as m
import PyQt5
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QSlider, QLabel, QVBoxLayout, QHBoxLayout, \
    QSizePolicy
import serial
import serial.tools.list_ports
import numpy as np


def findPort():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(port.device, port.description)
        if "USB" in port.description or "Arduino" in port.description or "ACM" in port.description:
            return port.device
    return None


def calcDelay(targetDelay):
    startDeleay = 2000
    x = np.linspace(-6,6, 200)
    sigmond = 1/(1+np.exp(-x))  #Broadcahst nupmy rechnet für alle Elementer der liste
    delays = startDeleay - (sigmond*(startDeleay - targetDelay))

    return [int(delay) for delay in delays]

port = findPort()
if port:
    ser = serial.Serial(port , 115200)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stepper-Motor-Calibration")
        widget = QWidget()
        self.setCentralWidget(widget)
        self.setMinimumSize(709, 164)


        #---Slider Widghet---
        self.Slider = QSlider(Qt.Horizontal)
        self.Slider.setRange(0, 6000)

        #---slider Lable
        label = (QLabel(f"RPM: 0"))
        self.Slider.valueChanged.connect(lambda v: label.setText(f"RPM: {v}"))
        label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)



        #---Start-Button-Widget
        startButton = QPushButton("Start")
        startButton.clicked.connect(self.sendRPmicS)


        #---Stop Button Widget---
        stopButton = QPushButton("Stop")
        stopButton.clicked.connect(self.sendStop)


        #---Layout


        layout1 = QVBoxLayout()
        layout1.addWidget(label)
        layout1.addWidget(self.Slider)
        layout3 = QHBoxLayout()
        layout3.addWidget(startButton)
        layout3.addWidget(stopButton)
        layout1.addLayout(layout3)

        widget.setLayout(layout1)

    def sendRPmicS(self):
        #---RPM to delay---
        RPM = self.Slider.value()
        if RPM > 0:
            StepsPerRound = 200 * 8 #Schritte für eine Umdreheung mit Microschritten
            RPS = RPM / 60
            StepsPerSecond = RPS * StepsPerRound
            delay_us = int(1_000_000 / StepsPerSecond)
            delayList = calcDelay(delay_us)
            data = ",".join(map(str, delayList))

            if port:
                ser.write(f"Delay:{data}\n".encode())
                print("data send")
            else:
                print("no port".encode())

    def sendStop(self):
        if port:

            ser.write("Stop".encode())
        else:
            print("No Serial Port Found")

    def closeEvent(self, event):
        print(self.width(), self.height())
        event.accept()



app = QApplication(sys.argv)
window = MainWindow()
window.show()

print(window.width(), window.height())
app.exec_()