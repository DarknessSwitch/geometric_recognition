from PyQt5.QtWidgets import QMainWindow, QTabWidget
from gui.generated.ui_main_window import Ui_MainWindow
from gui.sound_picker import SoundPicker
from gui.options_page import OptionsPage
from threading import Thread


class MainWindow(QMainWindow):

    def __init__(self, camera, sound_player):
        super(MainWindow, self).__init__()
        self.camera = camera
        self.sound_picker = SoundPicker(sound_player)
        self.options_page = OptionsPage(camera)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(722, 611)
        self.ui.tabWidget.clear()
        self.ui.tabWidget.addTab(self.sound_picker, 'Sound picker')
        self.ui.tabWidget.addTab(self.options_page, 'Options page')
        self.run_camera()

    def run_camera(self):
        Thread(target=self.camera.run).start()