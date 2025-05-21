import time
import os
import pyperclip
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPixmap
from upload_api import UpLoadAPI
from message_box import MessageBox

class DropImageWidget(QWidget):
  def __init__(self, github_settings_dic, normal_settings_dic):
    super().__init__()
    self.setFixedSize(600, 500)
    self.setStyleSheet("""
    QWidget {
      background-color: #2C2A38;
    }""")
    layout = QVBoxLayout(self)
    layout.setContentsMargins(30, 30, 30, 30)
    layout.setSpacing(30)

    title = QLabel("image upload")
    title.setStyleSheet("""
                        QLabel { 
                        font-size: 24px;
                        font-weight: bold;
                        color: #ffffff;
                        }""")
    title.setAlignment(Qt.AlignCenter)

    self.image_label = QLabel("drag and drop images here")
    self.image_label.setAlignment(Qt.AlignCenter)
    self.image_label.setStyleSheet("""
            QLabel {
            border: 2px dashed #aaa;
            border-radius: 10px;
            qproperty-alignment: AlignCenter;
            min-height: 300px;
            width: 200px;
            color: #ffffff;
            font-size: 20px;
            }""")
    self.image_label.setAcceptDrops(True)

    title.setAlignment(Qt.AlignCenter)
    self.upload_button = QPushButton("upload")
    self.upload_button.setFixedSize(540, 50)
    self.upload_button.setStyleSheet("""
    QPushButton {
      margin: 0px 200px 0px 200px;
      font-size: 20px;
      color: #ffffff;
      background-color: #606068;
      border-radius: 5px;
    }
    QPushButton:hover {
      background-color: #808088;
    }""")
    self.upload_button.clicked.connect(self.upload)

    layout.addWidget(title)
    layout.addWidget(self.image_label)
    layout.addWidget(self.upload_button)

    self.setAcceptDrops(True)

    self.github_settings_dic = github_settings_dic

    self.normal_settings_dic = normal_settings_dic
    self.image_name = ""

  def dragEnterEvent(self, event):
    if event.mimeData().hasUrls():
      url = event.mimeData().urls()[0]
      file_path = url.toLocalFile()
      if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        event.acceptProposedAction()
  
  def dropEvent(self, event):
    for url in event.mimeData().urls():
      self.image_name = os.path.basename(url.toLocalFile())
      self.image_path = url.toLocalFile()
      file_path = url.toLocalFile()
      if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
          self.current_image_path = file_path
          self.image_label.setPixmap(pixmap.scaled(
            self.image_label.width(), 
            self.image_label.height(), 
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
          ))
          break
        else:
          MessageBox.information(None, "error", "unable to load image file")

  def upload(self):
    if self.image_name == "":
      MessageBox.information(None, "failed", "you haven't added any images yet")
      return
    self.upload_button.setEnabled(False)
    if self.normal_settings_dic["rename before upload"] and self.normal_settings_dic["rename with timestamp"]:
      timestamp_ms = int(time.time() * 1000)
      self.image_name = str(timestamp_ms) + os.path.splitext(self.image_name)[1]

    self.worker = UpLoadAPI(self.github_settings_dic)
    self.t = QThread()
    self.worker.moveToThread(self.t)
    self.worker.set_image(self.image_path, self.image_name, self.show_func)
    self.worker.finished_func.connect(self.upload_finished)
    self.worker.finished_func.connect(self.worker.deleteLater)

    self.t.started.connect(self.worker.upload)
    self.t.finished.connect(self.t.deleteLater)
    self.t.start()

  def upload_finished(self, state):
    if state:
      pyperclip.copy(self.github_settings_dic['domain'] + self.image_name)
    self.upload_button.setEnabled(True)
    self.t.quit()

  def update_normal_settings(self, normal_settings_dic):
    self.normal_settings_dic = normal_settings_dic
  
  def update_github_settings(self, github_settings_dic):
    self.github_settings_dic = github_settings_dic

  def show_func(self, title, message):
    MessageBox.information(None, title, message)
