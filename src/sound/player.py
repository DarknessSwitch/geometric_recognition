import pyaudio
import wave
import time


class Player:

    def __init__(self, filepath):
        self.filepath = filepath
        self.p = pyaudio.PyAudio()
        self.wf = wave.open(self.filepath, 'rb')


    # define callback (2)
    def callback(self, in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)
        return (data, pyaudio.paContinue)


    def play(self):
        # open stream using callback (3)
        stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                        channels=self.wf.getnchannels(),
                        rate=self.wf.getframerate(),
                        output=True,
                        stream_callback=self.callback)
        # start the stream (4)
        stream.start_stream()

        # wait for stream to finish (5)
        while stream.is_active():
            time.sleep(0.01)

        # stop stream (6)
        stream.stop_stream()
        stream.close()
        self.wf.close()

        # close PyAudio (7)
        self.p.terminate()
