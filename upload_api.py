import requests
import base64
from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal

class UpLoadAPI(QObject):
  finished_func = pyqtSignal(bool)
  def __init__(self, settings_dic):
    super().__init__()
    self.update_settings(settings_dic)

  def upload(self):
    with open(self.img_path, "rb") as image_file:
      content = base64.b64encode(image_file.read()).decode("utf-8")
    self.data["message"] = f"add image via GitPic - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    self.data["content"] = content
    url = self.url + self.img_rename
    try:
      response = requests.put(url, json=self.data, headers=self.headers, timeout=5)
      if response.status_code == 201:
        self.show_func("success", "the image link has been copied to the clipboard")
        self.finished_func.emit(True)
        return
      else:
        self.show_func("failed", "upload failed")
    except requests.exceptions.Timeout:
      self.show_func("failed", "upload timeout")
    except requests.exceptions.ConnectionError:
      self.show_func("failed", "connect failed")
    self.finished_func.emit(False)
  
  def set_image(self, img_path, img_rename, show_func):
    self.img_path = img_path
    self.img_rename = img_rename
    self.show_func = show_func

  def update_settings(self, settings_dic):
    token = settings_dic["token"]
    repo = settings_dic["reposity"]
    branch = settings_dic["branch"]
    path = settings_dic["path"]
    if path == "":
      self.url = f"https://api.github.com/repos/{repo}/contents/"
    else:
      path = path.strip("/")
      self.url = f"https://api.github.com/repos/{repo}/contents/{path}/"
    self.headers = {
      "Authorization": f"token {token}",
      "Accept": "application/vnd.github.v3+json"
    }
    self.data = {
      "branch": branch
    }
