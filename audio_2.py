import os
import sys

from PyQt5 import QtCore, QtWidgets, QtMultimedia

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

app = QtWidgets.QApplication(sys.argv)

recorder = QtMultimedia.QAudioRecorder()

selected_audio_input = recorder.audioInput()

print("Audio Inputs:")
for i, audio_input in enumerate(recorder.audioInputs()):
    print(f"{i}. {audio_input}")

recorder.setAudioInput(selected_audio_input)

settings = QtMultimedia.QAudioEncoderSettings()

selected_codec = "audio/pcm"
print("Codecs:")
for i, codec in enumerate(recorder.supportedAudioCodecs()):
    print(f"{i}. {codec}")

print(f"selected codec:{selected_codec}")
settings.setCodec(selected_codec)

selected_sample_rate = 0
print("Sample rates:")
sample_rates, continuous = recorder.supportedAudioSampleRates()
for i, sample_rate in enumerate(sample_rates):
    print(f"{i}. {sample_rate}")
settings.setSampleRate(selected_sample_rate)

bit_rate = 32000  # other values: 32000, 64000,96000, 128000
settings.setBitRate(bit_rate)

channels = 1  # other values: 1, 2, 4
settings.setChannelCount(channels)
settings.setQuality(QtMultimedia.QMultimedia.NormalQuality)
settings.setEncodingMode(QtMultimedia.QMultimedia.ConstantBitRateEncoding)
print("micro",selected_audio_input)
print ("Sample rates selected",selected_sample_rate)
print(QtMultimedia.QMultimedia.ConstantBitRateEncoding)


print("Containers")
selected_container = ""
for i, container in enumerate(recorder.supportedContainers()):
    print(f"{i}. {container}")

recorder.setEncodingSettings(
    settings, QtMultimedia.QVideoEncoderSettings(), selected_container
)

filename = os.path.join(CURRENT_DIR, "test.mp3")
print(filename)
recorder.setOutputLocation(QtCore.QUrl.fromLocalFile(filename))


def handle_durationChanged(progress):
    print(f"progress: {progress/1000} seg")


def handle_statusChanged(status):
    if status == QtMultimedia.QMediaRecorder.FinalizingStatus:
        QtCore.QTimer.singleShot(1 * 1000, QtCore.QCoreApplication.quit)


recorder.durationChanged.connect(handle_durationChanged)
recorder.statusChanged.connect(handle_statusChanged)


def handle_timeout():
    recorder.stop()


QtCore.QTimer.singleShot(10 * 1000, handle_timeout)
print("Enregistrement en cours")
recorder.record()
print("Enregistrement Terminé")

sys.exit(app.exec_())