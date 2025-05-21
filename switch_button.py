from PyQt5.QtCore import Qt, QRect, QPoint, QVariantAnimation
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget

class SwitchButton(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setFixedSize(50, 30)
    self.checked = False
    self.setCursor(Qt.PointingHandCursor)
    self.animation = QVariantAnimation()
    self.animation.setDuration(80)
    self.animation.setStartValue(0)
    self.animation.setEndValue(20)
    self.animation.valueChanged.connect(self.update)

  def set_checked(self, check):
    self.checked = check
    self.animation.setDirection(QVariantAnimation.Forward if self.checked else QVariantAnimation.Backward)
    self.animation.start()

  def paintEvent(self, event):
    painter = QPainter(self)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setPen(Qt.NoPen)
    painter.setBrush(QColor('#07c160') if self.checked else QColor('#d5d5d5'))
    painter.drawRoundedRect(QRect(0, 0, self.width(), self.height()), 15, 15)
    offset = self.animation.currentValue()
    painter.setBrush(QColor(255, 255, 255))
    painter.drawEllipse(QPoint(15 + offset, 15), 12, 12)

  def mouseReleaseEvent(self, event):
    if event.button() == Qt.LeftButton:
      self.checked = not self.checked
      self.animation.setDirection(QVariantAnimation.Forward if self.checked else QVariantAnimation.Backward)
      self.animation.start()

  def connect_func(self, func):
    self.animation.finished.connect(func)
