from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QLayout, QWidget
from src.engine.world import world
from PySide6.QtGui import QKeyEvent
import os, re
import src.accountManager.accounts as accounts
ACCOUNTS = accounts.getAccountContext()
class gameWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.world = None
        self.keys_held = []
        self.pr = None
        self.defaultLayout = None
    def setLayout(self, arg__1: QLayout) -> None:
        if not self.defaultLayout:
            self.defaultLayout = arg__1
        return super().setLayout(arg__1)
    def initworld(self, file):
        self.world = world(self, file)
        self.update()
    def get_all_levels(self, mappack=None) -> list[str]: #mappack is NOT USED!
        files = os.listdir("src/maps/")
        ffiles = []
        for file in files:
            if re.match(r"^[a-zA-Z0-9_\-\() ]+.ptb$",file):
                ffiles.append(file)
        return ffiles
    def start_level(self, level: str) -> None:
        self.world = world(self, level)
    def get_completed(self, level: str) -> bool:
        if ACCOUNTS.user_content == None:
            return False
        return ACCOUNTS.user_content.is_level_completed(f"src/maps/{level}")
    def api_get_runtime(self) -> tuple[int, int, int, int, int]:
        days = 0
        hours = 0
        minutes = 0
        seconds = 0
        millies = 0
        if self.world == None:
            return (0,0,0,0,0)
        runtime = self.world.runtime
        millies = (runtime % 20) * 50
        runtime = int(runtime/20)
        seconds = (runtime % 60)
        runtime = int(runtime/60)
        minutes = (runtime % 60)
        runtime = int(runtime/60)
        hours = (runtime%24)
        runtime = int(runtime/24)
        days = runtime
        return (days, hours, minutes, seconds, millies)
    def api_get_time(self, levelname):
        if ACCOUNTS.user_content == None:
            return "-"
        return ACCOUNTS.user_content.get_time(levelname)
    def api_get_all_times(self, levelfolder="src/maps/") -> list[str]:
        if ACCOUNTS.user_content == None:
                return "-"
        res = []
        for file in os.listdir(levelfolder):
            if file.endswith(".ptb"):
                if self.get_completed(levelfolder + file):
                    res.append(self.api_get_time(levelfolder + file))
        return res
    def parenthook(self, prnt):
        self.pr = prnt
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        if self.world:
            self.world.paintEvent(painter)
        painter.end()
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() not in self.keys_held:
            self.keys_held.append(event.key())
    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if event.key() in self.keys_held:
            self.keys_held.remove(event.key())