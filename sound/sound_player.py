from sound.player import Player
import threading
from os import path


class SoundPlayer:

    def __init__(self, event_emitter):
        self.threads = []
        self.event_emitter = event_emitter
        self.event_emitter.on(self.event_emitter.event_name, self.on_prediction)
        self.prev_prediction = ''
        self.repeat_same = False
        self.sound_dict = {'1': None, '2': None, '3': None, '4': None, '5': None, 'Fist': None, 'Palm': None}
        self.set_sound('Palm', path.normpath('D:\Samples\Ableton_samples\Drums\FX Hit\FX Scratch Slackjaw.wav'))
        self.set_sound('Fist', path.normpath('D:\Samples\Ableton_samples\\16bit\Synth\JX Chorus Bass.wav'))

    def on_prediction(self, prediction):
        if (prediction == self.prev_prediction and self.repeat_same) or prediction != self.prev_prediction:
            self.play_sign(prediction)
            self.prev_prediction = prediction

    def clear_sound(self, sign):
        self.sound_dict[sign] = None

    def set_sound(self, sign, filepath):
        try:
            self.sound_dict[sign] = path.normpath(filepath)
            return True
        except Exception as ex:
            print(ex)
            return False

    def play(filepath):
        player = Player(filepath)
        thread = threading.Thread(target=player.play)
        thread.start()

    def play_sign(self, sign):
        if sign is not None and sign != ''\
                and self.sound_dict[sign] is not None and self.sound_dict[sign] != '':
            SoundPlayer.play(self.sound_dict[sign])
