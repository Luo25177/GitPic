from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt

class SideBar(QWidget):
  def __init__(self, width):
    super().__init__()

    self.setFixedWidth(width)

    self.setStyleSheet("""
    QWidget {
      background-color: #42424E;
    }""")

    sidebar_layout = QVBoxLayout(self)
    sidebar_layout.setContentsMargins(0, 0, 0, 0)
    sidebar_layout.setSpacing(0)

    self.sidebar_list = QListWidget()
    self.sidebar_list.setStyleSheet("""
    QListWidget {
      border: none;
      font-size: 24px;
    }
    QListWidget::item {
      padding: 10px 15px;
      height: 30px;
      color: #CAD4D4;
      border-radius: 5px;
    }
    QListWidget::item:hover {
      background-color: #808088;
    }
    QListWidget::item:selected {
      background-color: #2C2A38;
      color: #FFFFFF;
    }
    QListWidget:focus
    {
        outline: 0px;
    }""")

    sidebar_layout.addWidget(self.sidebar_list)

  def connect_func(self, func):
    self.sidebar_list.currentRowChanged.connect(func)

  def set_item(self, text, page_name):
    item = QListWidgetItem(text)
    item.setData(Qt.UserRole, page_name)
    item.setTextAlignment(Qt.AlignCenter) 
    self.sidebar_list.addItem(item)

  def set_current(self, page_name):
    self.sidebar_list.setCurrentRow(page_name)
  
