import struct

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import usb.core
import usb.util

class UsbConnection(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.connectionLabel = QLabel("Device not found!")
        self.layout.addWidget(self.connectionLabel)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.device = None
        self.configuration = None
        self.interface = None
        self.inEndpoint = None
    def ConnectUSB(self, vendorId, productId):
        self.device = usb.core.find(idVendor=vendorId, idProduct=productId)

        if self.device is None:
            self.connectionLabel.setText("Device not found!")
            return

        self.configuration = self.device.get_active_configuration()
        self.interface = self.configuration[(0, 0)]

        self.inEndpoint = usb.util.find_descriptor(
            self.interface,
            custom_match= \
                lambda e: \
                    usb.util.endpoint_direction(e.bEndpointAddress) == \
                    usb.util.ENDPOINT_IN)

        if self.inEndpoint is None:
            return

        self.connectionLabel.setText(f"Connected to {self.device.product}")

    def SendFeatureReport(self, packet):
        packetLen = len(packet)
        if (packetLen < 64):
            for x in range(64 - packetLen):
                packet.append(0)

        # send ctrl transfer
        self.device.ctrl_transfer(0x21, 0x09, 0x0300, 0x0000, packet)
        print("Data sent!")
        # usb.util.dispose_resources(dev)   if there are errors try this

