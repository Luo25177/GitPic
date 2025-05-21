import requests
from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal

class DeleteAPI(QObject):
  finished_func = pyqtSignal(bool, int)

  def __init__(self):
    super().__init__()

  def setup(self, path, show_func, settings_dic, index):
    self.show_func = show_func
    self.index = index

    token = settings_dic["token"]
    repo = settings_dic["reposity"]
    branch = settings_dic["branch"]
    self.url = f"https://api.github.com/repos/{repo}/contents/{path}"
    self.headers = {
      "Authorization": f"token {token}",
      "Accept": "application/vnd.github.v3+json"
    }
    self.data = {
      "branch": branch
    }


  def delete_work(self):
    response = requests.get(self.url, headers = self.headers)
    
    if response.status_code != 200:
      self.show_func("failed", "failed to get file information")
      self.finished_func.emit(False, self.index)
    else:
      file_info = response.json()
      sha = file_info['sha']
      self.data["sha"] = sha
      self.data["message"] = f"delete image via GitPic - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
      delete_response = requests.delete(self.url, headers=self.headers, json=self.data)
      if delete_response.status_code == 200:
        self.show_func("success", "file deleted successfully")
        self.finished_func.emit(True, self.index)
      else:
        self.show_func("failed", "file deletion failed")
        self.finished_func.emit(False, self.index)
