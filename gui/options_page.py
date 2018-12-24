from PyQt5.QtWidgets import QWidget
from gui.generated.ui_options import Ui_OptionsPage


class OptionsPage(QWidget):

    def __init__(self, camera):
        self.camera = camera
        super(OptionsPage, self).__init__()
        self.ui = Ui_OptionsPage()
        self.ui.setupUi(self)
        self.init_callbacks()
        self.init_offsets()

    def init_callbacks(self):
        self.ui.checkBox_mute.stateChanged.connect(self.on_mute_changed)
        self.ui.checkBox_inputWindow.stateChanged.connect(self.on_input_changed)
        self.ui.checkBox_hsvWindow.stateChanged.connect(self.on_hsv_changed)
        self.ui.checkBox_maskWindow.stateChanged.connect(self.on_mask_changed)
        self.ui.checkBox_Draw.stateChanged.connect(self.on_draw_changed)

        self.ui.horizontalSlider_hl.valueChanged.connect(self.on_hl_change)
        self.ui.horizontalSlider_sl.valueChanged.connect(self.on_sl_change)
        self.ui.horizontalSlider_vl.valueChanged.connect(self.on_vl_change)
        self.ui.horizontalSlider_hu.valueChanged.connect(self.on_hu_change)
        self.ui.horizontalSlider_su.valueChanged.connect(self.on_su_change)
        self.ui.horizontalSlider_vu.valueChanged.connect(self.on_vu_change)

    def init_offsets(self):
        self.ui.label_hl.setText(str(self.camera.l_offset[0]))
        self.ui.label_sl.setText(str(self.camera.l_offset[1]))
        self.ui.label_vl.setText(str(self.camera.l_offset[2]))

        self.ui.label_hu.setText(str(self.camera.h_offset[0]))
        self.ui.label_su.setText(str(self.camera.h_offset[1]))
        self.ui.label_vu.setText(str(self.camera.h_offset[2]))

        self.ui.horizontalSlider_hl.setValue(self.camera.l_offset[0])
        self.ui.horizontalSlider_sl.setValue(self.camera.l_offset[1])
        self.ui.horizontalSlider_vl.setValue(self.camera.l_offset[2])

        self.ui.horizontalSlider_hu.setValue(self.camera.h_offset[0])
        self.ui.horizontalSlider_su.setValue(self.camera.h_offset[1])
        self.ui.horizontalSlider_vu.setValue(self.camera.h_offset[2])

    def on_mute_changed(self, state):
        self.camera.set_mute(state == 2)

    def on_input_changed(self, state):
        self.camera.set_show_input(state == 2)

    def on_hsv_changed(self, state):
        self.camera.set_show_hsv(state == 2)

    def on_mask_changed(self, state):
        self.camera.set_show_mask(state == 2)

    def on_draw_changed(self, state):
        self.camera.set_draw_geometry(state == 2)

    def on_hl_change(self, value):
        self.ui.label_hl.setText(str(value))
        self.camera.l_offset[0] = value

    def on_sl_change(self, value):
        self.ui.label_sl.setText(str(value))
        self.camera.l_offset[1] = value

    def on_vl_change(self, value):
        self.ui.label_vl.setText(str(value))
        self.camera.l_offset[2] = value

    def on_hu_change(self, value):
        self.ui.label_hu.setText(str(value))
        self.camera.h_offset[0] = value

    def on_su_change(self, value):
        self.ui.label_su.setText(str(value))
        self.camera.h_offset[1] = value

    def on_vu_change(self, value):
        self.ui.label_vu.setText(str(value))
        self.camera.h_offset[2] = value
