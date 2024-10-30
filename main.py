import struct

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import math
import ColourSelector as cs
import LEDGraphicsItem as lgi
import UsbConnection as usbConn
class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.vendorId = 0x1208
        self.productId = 0xECC1

        self.setWindowTitle('LED Circle Light')
        self.setFixedSize(600, 600)

        self.mainLayout = QVBoxLayout()
        lightingLayout = QGridLayout()

        self.circleView = QGraphicsView()
        self.circleScene = QGraphicsScene()
        self.colourPicker1 = cs.ColourSelectWidget(QColor(255, 0, 0))
        self.selectAllHotkey = QShortcut(QKeySequence("Ctrl+A"), self.circleView)
        self.usbDeviceConnection = usbConn.UsbConnection()
        self.reconnectButton = QPushButton("Retry Connection")

        self.circleView.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.ledCircles = []

        numLeds = 16
        circleRadius = 24
        divisions = (2 * math.pi) / numLeds
        outerRadius = 75.0

        for i in range(numLeds):
            x = outerRadius * math.sin(divisions * i)
            y = outerRadius * math.cos(divisions * i)

            circle = lgi.LEDGraphicsItem(x, y, circleRadius, QColor(255, 0, 0, 255), i)

            self.ledCircles.append(circle)
            self.circleScene.addItem(circle)

        self.circleView.setScene(self.circleScene)


        lightingLayout.addWidget(self.circleView, 0, 1)

        horizontalSpacerLeft = QSpacerItem(125, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        horizontalSpacerRight = QSpacerItem(125, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        lightingLayout.addWidget(QLabel('LED Colour'), 2, 0)
        lightingLayout.addItem(horizontalSpacerLeft, 3, 0)
        lightingLayout.addItem(horizontalSpacerRight, 3, 2)
        lightingLayout.addWidget(self.colourPicker1, 3, 1)
        lightingLayout.addWidget(QLabel("Device Status:"), 4, 0)
        lightingLayout.addWidget(self.usbDeviceConnection, 4, 1)
        lightingLayout.addWidget(self.reconnectButton, 4, 2)

        self.mainLayout.addLayout(lightingLayout)

        # Submit
        self.sendButton = QPushButton('Send to Device')

        self.mainLayout.addWidget(self.sendButton)


        self.usbDeviceConnection.ConnectUSB(self.vendorId, self.productId)

        # Connections
        self.circleScene.selectionChanged.connect(self.LedSelectionChanged)
        self.colourPicker1.colourSelectionChanged.connect(self.ColourSelected)
        self.selectAllHotkey.activated.connect(self.SelectAllLeds)
        self.sendButton.released.connect(self.SendData)
        self.reconnectButton.released.connect(self.RetryUSBConnection)

        self.setLayout(self.mainLayout)

    def SelectAllLeds(self):
        items = self.circleScene.items()
        for led in items:
            led.setSelected(True)
    def LedSelectionChanged(self):
        items = self.circleScene.selectedItems()
        if(len(items) > 0):
            self.colourPicker1.SetBoxColour(items[0].getColour())

    def ColourSelected(self, colour):
        for leds in self.circleScene.selectedItems():
            leds.setColour(colour)

    def RetryUSBConnection(self):
        self.usbDeviceConnection.ConnectUSB(self.vendorId, self.productId)
    def SendData(self):
        dataToSend = []
        for leds in self.ledCircles:
            r = leds.getColour().red()
            g = leds.getColour().green()
            b = leds.getColour().blue()
            dataToSend.append(r)
            dataToSend.append(g)
            dataToSend.append(b)

        self.usbDeviceConnection.SendFeatureReport(dataToSend)


app = QApplication([])
app.setStyleSheet('''
    QWidget
    {
        font-size: 14px
    }
''')

window = Window()
window.show()

app.exec()

