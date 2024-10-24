from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class LEDGraphicsItem(QGraphicsEllipseItem):
    def __init__(self, x, y, diameter, colour, id):
        super().__init__(x, y, diameter, diameter)

        self.currentBrush = QBrush(colour, Qt.BrushStyle.SolidPattern)
        self.currentPen = self.pen()
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        self.id = id
        self.setBrush(self.currentBrush)
        self.setRect(x, y, diameter, diameter)

    def getId(self):
        return self.id

    def getColour(self):
        return self.currentBrush.color()

    def setColour(self, colour : QColor):
        self.currentBrush = QBrush(colour, Qt.BrushStyle.SolidPattern)
        self.setBrush(self.currentBrush)
        self.update()

    #def paint(self, painter, option, widget):
        #if(self.isSelected()):
          #  painter.drawRect(int(self.x()), int(self.y()), 28, 28)

        #option.state = QStyle.StateFlag.State_None
        #super().paint(painter, option, widget)

    def hoverEnterEvent(self, event : QGraphicsSceneHoverEvent):
        pen = QPen()
        pen.setWidth(self.currentPen.width() * 3)
        self.setPen(pen)
        self.update()

    def hoverLeaveEvent(self, event : QGraphicsSceneHoverEvent):
        self.setPen(self.currentPen)
        self.update()



