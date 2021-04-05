import os
import sys
from PyQt5 import QtCore, QtWidgets, QtMultimedia
from PyQt5.QtWidgets import QApplication, QDockWidget, QFileDialog, QMessageBox
from PyQt5 import uic
from PyQt5.QtMultimedia import QAudioDeviceInfo,QAudio,QCameraInfo
app = QApplication(sys.argv)
recorder = QtMultimedia.QAudioRecorder()

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(CURRENT_DIR, "test.mp3")

settings = QtMultimedia.QAudioEncoderSettings()

selected_codec = "audio/pcm"
settings.setCodec(selected_codec)


settings.setQuality(QtMultimedia.QMultimedia.VeryHighQuality)

selected_container = "mp3"
recorder.setEncodingSettings(settings, QtMultimedia.QVideoEncoderSettings(), selected_container)


def record():
    print("record")
    recorder.record()


def stop():
    print("stop")
    recorder.stop()


recorder.setOutputLocation(QtCore.QUrl.fromLocalFile(filename))
ui = uic.loadUi("recorder.ui")
ui.show()

ui.rec.clicked.connect(record)
ui.stop.clicked.connect(stop)

sys.exit(app.exec_())