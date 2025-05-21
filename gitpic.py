import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QApplication, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont, QPixmap

from sidebar import SideBar
from stack_page import StackPage
from my_enum import PageName

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("GitPic")
    self.setFixedSize(750, 550)
    self.setWindowFlag(Qt.FramelessWindowHint)
    self.setAttribute(Qt.WA_TranslucentBackground)
 
    self.setStyleSheet("""
    QWidget {
      background-color: #2C2A38;
    }""")   
 
    self.setAcceptDrops(True)

    self.main_widget = QWidget()
    self.main_widget.setFixedSize(750, 550)
    self.main_widget.setStyleSheet("""
      border-radius: 10px;
      background-color:#2C2A38;
    """)

    self.setCentralWidget(self.main_widget)

    self.main_layout = QVBoxLayout(self.main_widget)
    self.main_layout.setContentsMargins(0, 0, 0, 0)
    self.main_layout.setSpacing(0)

    self.title_widget = QWidget()
    self.title_widget.setFixedSize(750, 50)
    self.title_widget.setStyleSheet("""
      border-top-left-radius: 10px;
      border-top-right-radius: 10px;
      border-bottom-left-radius: 0px;
      border-bottom-right-radius: 0px;
      background-color: #343442;
    """)

    self.title_layout = QHBoxLayout(self.title_widget)
    self.title_layout.setContentsMargins(10, 5, 10, 5)
    self.title_layout.setSpacing(10)
    
    self.title_logo = QLabel()
    self.title_logo.setFixedSize(40, 40)
    pixmap = QPixmap("./img/logo.png")
    self.title_logo.setPixmap(pixmap)
    self.title_logo.setScaledContents(True)
    
    self.title_name = QLabel("GitPic")
    self.title_name.setFixedSize(620, 40)
    self.title_name.setStyleSheet("""
      font-size: 28px;
      color: #ffffff;
    """)

    self.title_button = QPushButton("×")
    self.title_button.setFixedSize(40, 40)
    self.title_button.setStyleSheet("""
      QPushButton {
        font-size: 30px;
        color: #ffffff;
        border-radius: 5px;
        background-color: #606068;
      }
      QPushButton:hover {
        background-color: #808088;
      }
    """)

    self.title_button.clicked.connect(self.close)

    self.title_layout.addWidget(self.title_logo)
    self.title_layout.addWidget(self.title_name)
    self.title_layout.addWidget(self.title_button)

    self.content_widget = QWidget()
    self.content_widget.setFixedSize(750, 500)
    self.content_widget.setStyleSheet("""
      border-top-left-radius: 0px;
      border-top-right-radius: 0px;
      border-bottom-left-radius: 10px;
      border-bottom-right-radius: 10px;
      background-color: #343442;
    """)

    self.content_layout = QHBoxLayout(self.content_widget)
    self.content_layout.setContentsMargins(0, 0, 0, 0)
    self.content_layout.setSpacing(0)

    self.sidebar = SideBar(150)
    self.content_layout.addWidget(self.sidebar)
    self.sidebar.set_item("upload", PageName.UpLoad)
    self.sidebar.set_item("Pics", PageName.Pics)
    self.sidebar.set_item("settings", PageName.Settings)
    self.sidebar.set_current(PageName.UpLoad.value)

    self.stack_page = StackPage()
    self.content_layout.addWidget(self.stack_page)
    self.stack_page.setCurrentIndex(PageName.UpLoad.value)

    self.sidebar.connect_func(self.change_page)

    self.main_layout.addWidget(self.title_widget)
    self.main_layout.addWidget(self.content_widget)

  def change_page(self, page_name):
    self.stack_page.setCurrentIndex(page_name)

  def mousePressEvent(self, event):
    if event.button() == Qt.LeftButton:
      self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
      event.accept()
  
  def mouseMoveEvent(self, event):
    if event.buttons() == Qt.LeftButton:
      self.move(event.globalPos() - self.drag_pos)
      event.accept()

if __name__ == "__main__":
  app = QApplication(sys.argv)

  font_path = "./fonts/MeriendaOne-Regular.ttf"
  font_id = QFontDatabase.addApplicationFont(font_path)
  font_families = QFontDatabase.applicationFontFamilies(font_id)
  custom_font = QFont(font_families[0])
  
  app.setFont(custom_font)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())
