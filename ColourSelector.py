from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class ColourSelectWidget(QWidget):
    colourSelectionChanged = pyqtSignal(QColor)

    def __init__(self, selectedColour):
        super().__init__()

        # Init components
        self.layout = QGridLayout()

        self.selectedColour = QColor(selectedColour)
        self.currentColourBox = QLabel()
        self.colourCircle = ColourCircle(selectedColour)
        self.redSpinBox = QSpinBox()
        self.greenSpinBox = QSpinBox()
        self.blueSpinBox = QSpinBox()
        self.hexLineEdit = QLineEdit()

        # Set properties
        self.redSpinBox.setRange(0, 255)
        self.greenSpinBox.setRange(0, 255)
        self.blueSpinBox.setRange(0, 255)
        self.hexLineEdit.setMaxLength(7)

        self.currentColourBox.setAutoFillBackground(True)
        pal = self.currentColourBox.palette()
        pal.setColor(self.currentColourBox.backgroundRole(), self.selectedColour)
        self.currentColourBox.setPalette(pal)
        self.currentColourBox.setFixedSize(64, 64)

        self.redSpinBox.setValue(self.selectedColour.red())
        self.greenSpinBox.setValue(self.selectedColour.green())
        self.blueSpinBox.setValue(self.selectedColour.blue())
        self.hexLineEdit.setText(self.selectedColour.name(QColor.NameFormat.HexRgb))

        # Connections
        self.colourCircle.colourChanged.connect(self.ColourWheelClicked)
        self.redSpinBox.valueChanged.connect(self.ColourSpinBoxChanged)
        self.greenSpinBox.valueChanged.connect(self.ColourSpinBoxChanged)
        self.blueSpinBox.valueChanged.connect(self.ColourSpinBoxChanged)
        self.hexLineEdit.editingFinished.connect(self.HexTextChanged)


        # Layout
        self.layout.addWidget(self.colourCircle, 0, 1)
        self.layout.addWidget(self.currentColourBox, 0, 2)
        self.layout.addWidget(QLabel('R'), 1, 0)
        self.layout.addWidget(self.redSpinBox, 1, 1, 1, 1)
        self.layout.addWidget(QLabel('G'), 2, 0)
        self.layout.addWidget(self.greenSpinBox, 2, 1, 1, 1)
        self.layout.addWidget(QLabel('B'), 3, 0)
        self.layout.addWidget(self.blueSpinBox, 3, 1, 1, 1)
        self.layout.addWidget(QLabel('Hex'), 4, 0)
        self.layout.addWidget(self.hexLineEdit, 4, 1, 1, 1)

        self.setLayout(self.layout)

    def GetSelectedColour(self):
        return self.selectedColour
    def SetBoxColour(self, colour):
        pal = self.currentColourBox.palette()
        pal.setColor(self.currentColourBox.backgroundRole(), colour)
        self.currentColourBox.setPalette(pal)

    def ColourWheelClicked(self, colour):
        self.selectedColour = colour
        self.SetBoxColour(colour)

        self.redSpinBox.blockSignals(True)
        self.greenSpinBox.blockSignals(True)
        self.blueSpinBox.blockSignals(True)

        self.redSpinBox.setValue(self.selectedColour.red())
        self.greenSpinBox.setValue(self.selectedColour.green())
        self.blueSpinBox.setValue(self.selectedColour.blue())
        self.hexLineEdit.setText(self.selectedColour.name())

        self.redSpinBox.blockSignals(False)
        self.greenSpinBox.blockSignals(False)
        self.blueSpinBox.blockSignals(False)

        self.colourSelectionChanged.emit(colour)

    def ColourSpinBoxChanged(self):
        colour = QColor()

        colour.setRgb(self.redSpinBox.value(), self.greenSpinBox.value(), self.blueSpinBox.value())
        self.selectedColour = colour
        self.hexLineEdit.setText(colour.name())
        self.SetBoxColour(colour)

        self.colourSelectionChanged.emit(colour)


    def HexTextChanged(self):
        colour = QColor(self.hexLineEdit.text())
        self.selectedColour = colour
        self.SetBoxColour(colour)

        self.redSpinBox.setValue(self.selectedColour.red())
        self.greenSpinBox.setValue(self.selectedColour.green())
        self.blueSpinBox.setValue(self.selectedColour.blue())

        self.colourSelectionChanged.emit(colour)



class ColourCircle(QWidget):
    colourChanged = pyqtSignal(QColor)

    def __init__(self, selectedColour):
        super().__init__()
        self.radius = 75
        self.setFixedSize(self.radius * 2, self.radius * 2)
        self.padding = 8
        self.hue = selectedColour.hueF()
        self.saturation = selectedColour.saturationF()
        self.value = selectedColour.valueF()

    def paintEvent(self, event : QPaintEvent):
        centre = QPointF(self.width() / 2, self.height() / 2)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setViewport(self.padding, self.padding, self.width() - (2 * self.padding),
                            self.height() - (2 * self.padding))

        hsvGradient = QConicalGradient(centre, 90)

        if self.isEnabled():
            for degrees in range(360):
                col = QColor.fromHsvF(degrees / 360, 1, self.value)
                hsvGradient.setColorAt(degrees / 360, col)

            gradientValue = QRadialGradient(centre, self.radius)
            gradientValue.setColorAt(0.0, QColor.fromHsvF(0.0, 0.0, self.value, 1.0))
            gradientValue.setColorAt(1.0, QColorConstants.Transparent)
        else:
            hsvGradient = QLinearGradient(QPointF(0, self.radius), QPointF(0, self.radius))
            hsvGradient.setColorAt(0, QColor(100, 100, 100))
            hsvGradient.setColorAt(1, QColor(128, 128, 128))



        painter.setPen(QColorConstants.Transparent)
        painter.setBrush(hsvGradient)
        painter.drawEllipse(self.rect())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:

            self.hue, self.saturation, self.value = self.GetColourFromXY(event.position().x(), event.position().y())
            self.x = event.position().x() / self.width()
            self.y = event.position().y() / self.height()

            colour = QColor()
            colour.setHsvF(self.hue, self.saturation, self.value)
            self.colourChanged.emit(colour)
            self.repaint()

    def GetColourFromXY(self, x, y):
        pointCentre = QPointF(self.rect().center())
        pointXY = QPointF(float(x), float(y))

        line = QLineF(pointCentre, pointXY)
        s = min(1.0, (line.length() / self.radius))
        h = (line.angle() - 90) / 360 % 1.
        return h, s, self.value