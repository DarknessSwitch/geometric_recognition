from gui.generated.ui_sound_picker import Ui_SoundPickerForm
from gui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication, QDialog
import sys
from image import camera, image_processor
from util.my_emitter import MyEmitter
from sound.sound_player import SoundPlayer


nsamples = 6
event_emitter = MyEmitter()
image_proc = image_processor.ImageProcessor(nsamples, event_emitter)
sound_pl = SoundPlayer(event_emitter)
cam = camera.Camera(image_proc)


app = QApplication(sys.argv)
main_window = MainWindow(cam, sound_pl)
main_window.show()
sys.exit(app.exec_())

