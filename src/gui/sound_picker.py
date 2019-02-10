from PyQt5.QtWidgets import QWidget, QFileDialog
from gui.generated.ui_sound_picker import Ui_SoundPickerForm
import os,sys


class SoundPicker(QWidget):

    def __init__(self, sound_player):
        super(SoundPicker, self).__init__()
        self.ui = Ui_SoundPickerForm()
        self.ui.setupUi(self)
        self.init_callbacks()
        self.sound_player = sound_player
        self.init_default_sounds()

    def init_default_sounds(self):
        files = []
        for (dir, _, filenames) in os.walk(os.path.join(sys.path[0], 'resources/default_sounds')):
            for file in filenames:
                files.append(os.path.join(dir, file))
        self.sound_player.set_sound('1', files[0])
        self.ui.textEdit_1.setText(files[0])
        self.sound_player.set_sound('2', files[1])
        self.ui.textEdit_2.setText(files[1])
        self.sound_player.set_sound('3', files[2])
        self.ui.textEdit_3.setText(files[2])
        self.sound_player.set_sound('4', files[3])
        self.ui.textEdit_4.setText(files[3])
        self.sound_player.set_sound('5', files[4])
        self.ui.textEdit_5.setText(files[4])
        self.sound_player.set_sound('Fist', files[5])
        self.ui.textEdit_6.setText(files[5])
        self.sound_player.set_sound('Palm', files[6])
        self.ui.textEdit_7.setText(files[6])


    def init_callbacks(self):
        self.ui.button_1.clicked.connect(self.on_one_clicked)
        self.ui.button_2.clicked.connect(self.on_two_clicked)
        self.ui.button_3.clicked.connect(self.on_three_clicked)
        self.ui.button_4.clicked.connect(self.on_four_clicked)
        self.ui.button_5.clicked.connect(self.on_five_clicked)
        self.ui.button_Fist.clicked.connect(self.on_fist_clicked)
        self.ui.button_Palm.clicked.connect(self.on_palm_clicked)
        self.ui.button_c1.clicked.connect(self.on_clear_one)
        self.ui.button_c2.clicked.connect(self.on_clear_two)
        self.ui.button_c3.clicked.connect(self.on_clear_three)
        self.ui.button_c4.clicked.connect(self.on_clear_four)
        self.ui.button_c5.clicked.connect(self.on_clear_five)
        self.ui.button_cFist.clicked.connect(self.on_clear_fist)
        self.ui.button_cPalm.clicked.connect(self.on_clear_palm)

    def set_sound_for_sign(self, sign, label):
        filename, _ = QFileDialog.getOpenFileName(filter='*.wav')

        if filename != '' and filename is not None:
            label.setText('')
            success = self.sound_player.set_sound(sign, filename)
            if success:
                label.setText(filename)

    def clear_sound_for_sign(self, sign, label):
        label.setText('')
        self.sound_player.clear_sound(sign)

    def on_one_clicked(self):
        self.set_sound_for_sign('1', self.ui.textEdit_1)

    def on_clear_one(self):
        self.clear_sound_for_sign('1', self.ui.textEdit_1)

    def on_two_clicked(self):
        self.set_sound_for_sign('2', self.ui.textEdit_2)

    def on_clear_two(self):
        self.clear_sound_for_sign('2', self.ui.textEdit_2)

    def on_three_clicked(self):
        self.set_sound_for_sign('3', self.ui.textEdit_3)

    def on_clear_three(self):
        self.clear_sound_for_sign('3', self.ui.textEdit_3)

    def on_four_clicked(self):
        self.set_sound_for_sign('4', self.ui.textEdit_4)

    def on_clear_four(self):
        self.clear_sound_for_sign('4', self.ui.textEdit_4)

    def on_five_clicked(self):
        self.set_sound_for_sign('5', self.ui.textEdit_5)

    def on_clear_five(self):
        self.clear_sound_for_sign('5', self.ui.textEdit_5)

    def on_fist_clicked(self):
        self.set_sound_for_sign('Fist', self.ui.textEdit_6)

    def on_clear_fist(self):
        self.clear_sound_for_sign('Fist', self.ui.textEdit_6)

    def on_palm_clicked(self):
        self.set_sound_for_sign('Palm', self.ui.textEdit_7)

    def on_clear_palm(self):
        self.clear_sound_for_sign('Palm', self.ui.textEdit_7)
