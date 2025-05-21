import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor

class MessageBox(QDialog):
  def __init__(self, title, infomation, parent=None):
    super().__init__(parent)
    self.setFixedSize(252, 202)
    
    self.setWindowFlags(Qt.FramelessWindowHint)
    self.setAttribute(Qt.WA_TranslucentBackground)
    layout = QHBoxLayout(self)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    back_widget = QWidget()
    back_widget.setFixedSize(252, 202)
    back_widget.setStyleSheet("""
      background-color: #ffffff;
      border-radius: 10px;
    """)
    
    layout.addWidget(back_widget)

    layout_back = QHBoxLayout(back_widget)
    layout_back.setContentsMargins(1, 1, 1, 1)
    layout_back.setSpacing(0)

    main_widget = QWidget()
    main_widget.setFixedSize(250, 200)
    main_widget.setStyleSheet("""
      color: #ffffff;
      border-radius: 10px;
      background-color: #ffffff;
    """)
    layout_back.addWidget(main_widget)

    v_layout = QVBoxLayout(main_widget)
    v_layout.setContentsMargins(0, 0, 0, 0)
    v_layout.setSpacing(0)

    title_widget = QWidget()
    title_widget.setFixedSize(250, 50)
    title_widget.setStyleSheet("""
      background-color: #42424e;
      font-size: 24px;
      border-top-left-radius: 10px;
      border-top-right-radius: 10px;
      border-bottom-left-radius: 0px;
      border-bottom-right-radius: 0px;
    """)

    title_h_layout = QHBoxLayout(title_widget)
    title_h_layout.setContentsMargins(10, 10, 10, 10)
    title_h_layout.setSpacing(20)

    title_text = QLabel(title)
    title_text.setFixedSize(230, 30)
    title_text.setAlignment(Qt.AlignVCenter)
    title_text.setStyleSheet("""
      border-radius: 5px;
    """)
    
    title_h_layout.addWidget(title_text)

    content_widget = QWidget()
    content_widget.setFixedSize(250, 150)
    content_widget.setStyleSheet("""
      background-color: #343442;
      font-size: 24px;
      border-top-left-radius: 0px;
      border-top-right-radius: 0px;
      border-bottom-left-radius: 10px;
      border-bottom-right-radius: 10px;
    """)

    content_v_layout = QVBoxLayout(content_widget) 
    content_v_layout.setContentsMargins(10, 10, 10, 10)
    content_v_layout.setSpacing(10)

    content_label = QLabel(infomation)
    content_label.setFixedSize(230, 80)
    content_label.setWordWrap(True)
    content_label.setStyleSheet("""
      padding: 5px;
      font-size: 16px;
      background-color: #606068;
      border-radius: 5px;
    """)
    
    content_button = QPushButton("OK")
    content_button.setFixedSize(230, 40)
    content_button.setStyleSheet("""
    QPushButton {
      margin: 0px 90px 0px 90px;
      background-color: #606068;
      font-size: 24px;
      border-radius: 5px;
    }
    QPushButton:hover {
      background-color: #808088;
    }
    """)
    content_button.clicked.connect(self.close)

    content_v_layout.addWidget(content_label)
    content_v_layout.addWidget(content_button)

    v_layout.addWidget(title_widget)
    v_layout.addWidget(content_widget)
      
  def setWindowTitle(self, title):
    self.title_label.setText(title)
      
  @classmethod
  def critical(cls, parent, title, text):
      dialog = cls(title, text, parent)
      return dialog.exec_()
      
  @classmethod
  def information(cls, parent, title, text):
      dialog = cls(title, text, parent)
      return dialog.exec_()

  def mousePressEvent(self, event):
    if event.button() == Qt.LeftButton:
      self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
      event.accept()
  
  def mouseMoveEvent(self, event):
    if event.buttons() == Qt.LeftButton:
      self.move(event.globalPos() - self.drag_pos)
      event.accept()
