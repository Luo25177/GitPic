import pyperclip
import requests
from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QListWidgetItem
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
from message_box import MessageBox
from delete_api import DeleteAPI

image_list_data = []
fail_information = ""

class WorkThread(QObject):
  get_image_func = pyqtSignal()
  finished_func = pyqtSignal()

  def __init__(self, github_settings_dic):
    super().__init__()
    self.update_settings(github_settings_dic)

  def update_settings(self, github_settings_dic):
    token = github_settings_dic["token"]
    repo = github_settings_dic["reposity"]
    branch = github_settings_dic["branch"]
    self.domain = github_settings_dic["domain"]

    self.headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    self.api_url = f"https://api.github.com/repos/{repo}/contents/"
    self.data = {
      "branch": branch
    }
  
  def get_images_from_github(self, path="/"):
    l = []
    global fail_information
    try:
      response = requests.get(f"{self.api_url}{path}", headers=self.headers, json=self.data, timeout=5)
      if response.status_code == 200:
        contents = response.json()
        for item in contents:
          if item['type'] == 'dir':
            l.extend(self.get_images_from_github(item['path']))
          elif item['path'].lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            response = requests.get(item['download_url'], headers=self.headers, json=self.data, timeout=5)
            l.append([item['path'], response.content])
      else:
        fail_information = "upload failed"
    except requests.exceptions.Timeout:
      fail_information = "upload timeout"
    except requests.exceptions.ConnectionError:
      fail_information = "connect failed"
    return l

  def do_work(self):
    global image_list_data
    image_list_data = self.get_images_from_github()
    self.finished_func.emit()

class ShowImageWidget(QWidget):
  def __init__(self, github_settings_dic):
    super().__init__()
    self.setFixedSize(600, 500)
    self.setStyleSheet("""
    QWidget {
      border-radius: 0px;
      background-color: #2C2A38;
    }""")
    
    self.v_layout = QVBoxLayout(self)
    self.v_layout.setContentsMargins(15, 15, 15, 15)
    self.v_layout.setSpacing(10)
    
    label = QLabel("loading")
    label.setStyleSheet("""
      font-size: 50px;
      color: #ffffff;
    """)
    label.setAlignment(Qt.AlignCenter) 
    self.v_layout.addWidget(label) 
    self.settings_dic = github_settings_dic

    self.worker = WorkThread(github_settings_dic)
    self.t = QThread()
    self.worker.moveToThread(self.t)
    self.worker.finished_func.connect(self.get_image_finished)
    self.worker.finished_func.connect(self.worker.deleteLater)
    
    self.t.started.connect(self.worker.do_work)
    self.t.finished.connect(self.t.deleteLater)
    self.t.start()
  
  def get_image_finished(self):
    self.t.quit()
    self.setup()
  
  def setup(self):
    for i in reversed(range(self.v_layout.count())): 
      self.v_layout.itemAt(i).widget().deleteLater()
    global image_list_data
    global fail_information
    self.index = len(image_list_data) - 1
    if len(image_list_data) == 0:
      self.label = QLabel(fail_information)
      self.label.setStyleSheet("""
        font-size: 50px;
        color: #ffffff;
      """)
      self.label.setAlignment(Qt.AlignCenter) 
      self.v_layout.addWidget(self.label)
    else:
      self.pic_list = QListWidget()
      self.pic_list.setStyleSheet("""
      QListWidget {
        border-radius: 5px;
        background-color: #2C2A38;
        qproperty-movement: Smooth;
        outline: 0;
      }
      QListWidget::item {
        height: 230px;
        color: #CAD4D4;
        font-size: 20px;
        border-radius: 5px;
      }
      QListWidget::item:hover {
        background-color: #808088;
      }
      QListWidget:focus
      {
          outline: 0px;
      }""")
      self.pic_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
      self.pic_list.setProperty("showItems", False)
      self.pic_list.setVerticalScrollMode(QListWidget.ScrollPerPixel)

      while self.index >= 0:
        item_widget = self.create_item_widget()
        item = QListWidgetItem()
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        self.pic_list.addItem(item)
        self.pic_list.setItemWidget(item, item_widget)
      
      self.v_layout.addWidget(self.pic_list)

    update_button = QPushButton("update")
    update_button.setStyleSheet("""
    QPushButton {
      font-size: 24px;
      color: #ffffff;
      background-color: #606068;
      border-radius: 5px;
    }
    QPushButton:hover {
      background-color: #808088;
    }""")
    update_button.setFixedSize(570, 40)
    update_button.clicked.connect(self.update)
    self.v_layout.addWidget(update_button)

  def create_item_widget(self):
    widget = QWidget()
    widget.setFixedSize(570, 230)
    widget.setStyleSheet("""
      background-color: #2C2A38;
    """)
    
    layout = QHBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    num = 3
    while num > 0:
      widget_item = self.create_sigal_item()
      if widget_item != None:
        layout.addWidget(widget_item)
        num -= 1
      elif self.index < 0:
        break
    layout.addStretch()
    return widget

  def create_sigal_item(self):
    widget = QWidget()
    widget.setFixedSize(190, 230)
    widget.setStyleSheet("""
      background-color: #2C2A38;
    """)

    v_layout = QVBoxLayout(widget)
    v_layout.setContentsMargins(10, 10, 10, 10)
    v_layout.setSpacing(10)

    if self.index < 0:
      return None

    global image_list_data
    pixmap = QPixmap()
    pixmap.loadFromData(image_list_data[self.index][1])
    if pixmap.isNull():
      return None
    
    label = QLabel()
    label.setFixedSize(170, 170)
    label.setPixmap(pixmap.scaled(
            label.width(), 
            label.height(), 
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation))

    h_layout = QHBoxLayout()
    h_layout.setContentsMargins(0, 0, 0, 0)
    h_layout.setSpacing(10)

    button_copy = QPushButton("copy url")
    button_copy.setFixedSize(90, 30)
    button_copy.setStyleSheet("""
    QPushButton {
      font-size: 20px;
      color: #ffffff;
      background-color: #606068;
      border-radius: 5px;
    }
    QPushButton:hover {
      background-color: #808088;
    }""")
    path = image_list_data[self.index][0]
    button_copy.clicked.connect(lambda: self.copy_url(path))

    button_delete = QPushButton("delete")
    button_delete.setFixedSize(70, 30)
    button_delete.setStyleSheet("""
    QPushButton {
      font-size: 20px;
      color: #ffffff;
      background-color: #606068;
      border-radius: 5px;
    }
    QPushButton:hover {
      background-color: #808088;
    }""")
    
    path = image_list_data[self.index][0]
    index = self.index
    button_delete.clicked.connect(lambda: self.delete_url(path, index))
    self.index = self.index - 1

    h_layout.addWidget(button_copy)
    h_layout.addWidget(button_delete)
    
    v_layout.addWidget(label)
    v_layout.addLayout(h_layout)

    return widget

  def copy_url(self, path):
    pyperclip.copy(self.settings_dic["domain"] + path)
    MessageBox.information("success", "the image link has been copied to the clipboard")
  
  def delete_url(self, url, index):
    self.worker_delete = DeleteAPI()
    self.worker_delete.setup(url, self.show_func, self.settings_dic, index)
    self.thread_delete = QThread()
    self.worker_delete.moveToThread(self.thread_delete)
    self.worker_delete.finished_func.connect(self.delete_finished)
    self.worker_delete.finished_func.connect(self.worker_delete.deleteLater)

    self.thread_delete.started.connect(self.worker_delete.delete_work)
    self.thread_delete.finished.connect(self.thread_delete.deleteLater)
    self.thread_delete.start()

  def delete_finished(self, state, index):
    self.thread_delete.quit()
    if state:
      del image_list_data[index]
      self.setup()

  def update(self):
    for i in reversed(range(self.v_layout.count())): 
        self.v_layout.itemAt(i).widget().deleteLater()

    label = QLabel("loading")
    label.setStyleSheet("""
      font-size: 50px;
      color: #ffffff;
    """)
    label.setAlignment(Qt.AlignCenter) 
    self.v_layout.addWidget(label) 

    self.worker = WorkThread(self.settings_dic)
    self.t = QThread()
    self.worker.moveToThread(self.t)
    self.t.started.connect(self.worker.do_work)
    self.worker.finished_func.connect(self.setup)
    self.worker.finished_func.connect(self.worker.deleteLater)
    self.t.finished.connect(self.t.deleteLater)
    self.t.start()
  
  def update_settings(self, github_settings_dic):
    self.worker.update_settings(github_settings_dic)

  def show_func(self, title, message):
    MessageBox.information(None, title, message)
