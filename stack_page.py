from PyQt5.QtWidgets import QStackedWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
import json
from switch_button import SwitchButton
from drop_image_widget import DropImageWidget
from show_img_widget import ShowImageWidget

class StackPage(QStackedWidget):
  def __init__(self):
    super().__init__()
    self.setStyleSheet("""
    QWidget {
      background-color: #2C2A38;
    }""")
    self.read_settings()
    self.create_upload_page()
    self.create_pics_page()
    self.create_settings_page()

  def read_settings(self):
    try:
      with open("./cache/github_settings.json", 'r', encoding='UTF-8') as f:
        self.github_settings_dic = json.load(f)
    except FileNotFoundError:
      self.github_settings_dic = {
        "reposity":"name/repo",
        "branch":"master",
        "token":"",
        "path":"test",
        "domain":"https://cdn.jsdelivr.net/gh/name/repo@master/test/",
      }
      with open("./cache/github_settings.json", 'w', encoding='UTF-8') as f:
        f.write(json.dumps(self.github_settings_dic, ensure_ascii=False))

    try:
      with open("./cache/normal_settings.json", 'r', encoding='UTF-8') as f:
        self.normal_settings_dic = json.load(f)
    except FileNotFoundError:
      self.normal_settings_dic = {
        "rename before upload":False,
        "rename with timestamp":False,
      }
      with open("./cache/normal_settings.json", 'w', encoding='UTF-8') as f:
        f.write(json.dumps(self.normal_settings_dic, ensure_ascii=False))

  def create_upload_page(self):
    self.upload_page = DropImageWidget(self.github_settings_dic, self.normal_settings_dic)
    self.addWidget(self.upload_page)

  def create_pics_page(self):
    self.pics_page = ShowImageWidget(self.github_settings_dic)
    self.addWidget(self.pics_page)
  
  def create_settings_page(self):
    page = QWidget()
    page.setStyleSheet("""
    QWidget {
      background-color: #2C2A38;
      color: #ffffff;
    }""")

    layout = QVBoxLayout(page)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(0)
    
    github_set_page = QWidget()
    github_set_page.setFixedSize(560, 282)
    github_set_page.setStyleSheet("""
    QWidget {
      background-color: #2C2A38;
      color: #ffffff;
    }""")
    github_set_layout = QVBoxLayout(github_set_page)
    github_set_layout.setContentsMargins(10, 10, 10, 10)
    github_set_layout.setSpacing(10)
    github_set_title = QLabel("github settings")
    github_set_title.setFixedSize(540, 32)
    github_set_title.setStyleSheet("""
    QLabel { 
      background-color: #2C2A38;
      font-size: 20px;
      font-weight: bold;
      color: #ffffff;
    }""")
    github_set_list = QListWidget()
    github_set_list.setStyleSheet("""
    QListWidget {
      font-size: 24px;
      padding: 10px 10px 10px 10px;
      border-radius: 5px;
      background-color: #606068;
    }
    QListWidget::item {
      height: 40px;
      color: #CAD4D4;
      border-radius: 5px;
    }
    QListWidget::item:hover {
      background-color: #808088;
    }
    QListWidget:focus
    {
        outline: 0px;
    }""")
    github_set_list.setFixedSize(540, 220)
    self.create_settings_key_value("reposity", self.github_settings_dic["reposity"], github_set_list)
    self.create_settings_key_value("branch", self.github_settings_dic["branch"], github_set_list)
    self.create_settings_key_value("token", self.github_settings_dic["token"], github_set_list)
    self.create_settings_key_value("path", self.github_settings_dic["path"], github_set_list)
    self.create_settings_key_value("domain", self.github_settings_dic["domain"], github_set_list)
    github_set_layout.addWidget(github_set_title)
    github_set_layout.addWidget(github_set_list)

    normal_set_page = QWidget()
    normal_set_page.setFixedSize(560, 162)
    normal_set_page.setStyleSheet("""
    QWidget {
      background-color: #2C2A38;
      color: #ffffff;
    }""")
    normal_set_layout = QVBoxLayout(normal_set_page)
    normal_set_layout.setContentsMargins(10, 10, 10, 10)
    normal_set_layout.setSpacing(10)
    normal_set_title = QLabel("normal settings")
    normal_set_title.setFixedSize(540, 32)
    normal_set_title.setStyleSheet("""
                        QLabel { 
                        background-color: #2C2A38;
                        font-size: 20px;
                        font-weight: bold;
                        color: #ffffff;
                        }""")
    normal_set_list = QListWidget()
    normal_set_list.setStyleSheet("""
    QListWidget {
      font-size: 24px;
      padding: 10px 10px 10px 10px;
      border-radius: 5px;
      background-color: #606068;
    }
    QListWidget::item {
      height: 40px;
      color: #CAD4D4;
      border-radius: 5px;
    }
    QListWidget::item:hover {
      background-color: #808088;
    }
    QListWidget:focus
    {
        outline: 0px;
    }""")
    normal_set_list.setFixedSize(540, 100)

    self.create_settings_key_bool("rename before upload", self.normal_settings_dic["rename before upload"], normal_set_list)
    self.create_settings_key_bool("rename with timestamp", self.normal_settings_dic["rename with timestamp"], normal_set_list)
    normal_set_layout.addWidget(normal_set_title)
    normal_set_layout.addWidget(normal_set_list)
    layout.addWidget(github_set_page)
    layout.addWidget(normal_set_page)
    self.addWidget(page)

  def create_settings_key_value(self, key, value, settings_list):
    item_widget = QWidget()
    item_widget.setFixedHeight(40)
    item_widget.setStyleSheet("""
    QWidget{
      background: transparent;
    }""")
    key_label = QLabel(key)
    key_label.setFixedSize(100, 30)
    key_label.setStyleSheet("""
      QLabel {
        font-size: 16px;
        background: transparent;
      }""")

    value_edit = QLineEdit()
    value_edit.setFixedSize(400, 30)
    value_edit.setText(value)
    value_edit.setStyleSheet("""
      QLineEdit {
        qproperty-alignment: 'AlignCenter';
        font-size: 16px;
        border-radius: 12px;
        background: #f0f0f0;
        color: #000000
      }
    """)
    value_edit.textChanged.connect(lambda text : self.text_change(text, key))
    
    item_layout = QHBoxLayout(item_widget)
    item_layout.setContentsMargins(10, 0, 10, 0)
    item_layout.setSpacing(0)
    item_layout.addWidget(key_label)
    item_layout.addWidget(value_edit)
    item_layout.setAlignment(Qt.AlignVCenter)

    item = QListWidgetItem()
    item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
    settings_list.addItem(item)
    settings_list.setItemWidget(item, item_widget)

  def create_settings_key_bool(self, key, value, settings_list):
    item_widget = QWidget()
    item_widget.setFixedHeight(40)
    item_widget.setStyleSheet("""
    QWidget{
      background: transparent;
    }""")
    key_label = QLabel(key)
    key_label.setFixedSize(450, 30)
    key_label.setStyleSheet("""
      QLabel {
        font-size: 16px;
        background: transparent;
      }""")

    value_edit = SwitchButton()
    value_edit.set_checked(value)
    value_edit.connect_func(lambda : self.switch_change(value_edit.checked, key))
    
    item_layout = QHBoxLayout(item_widget)
    item_layout.setContentsMargins(10, 0, 10, 0)
    item_layout.setSpacing(0)
    item_layout.addWidget(key_label)
    item_layout.addWidget(value_edit)
    item_layout.setAlignment(Qt.AlignVCenter)

    item = QListWidgetItem()
    item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
    settings_list.addItem(item)
    settings_list.setItemWidget(item, item_widget)
  
  def switch_change(self, value, key):
    self.normal_settings_dic[key] = value
    self.upload_page.update_normal_settings(self.normal_settings_dic)
    with open("./cache/normal_settings.json", 'w', encoding='UTF-8') as f:
       f.write(json.dumps(self.normal_settings_dic, ensure_ascii=False))

  def text_change(self, text, key):
    self.github_settings_dic[key] = text
    self.upload_page.update_github_settings(self.github_settings_dic)
    self.pics_page.update_settings(self.github_settings_dic)
    with open("./cache/github_settings.json", 'w', encoding='UTF-8') as f:
      f.write(json.dumps(self.github_settings_dic, ensure_ascii=False))
