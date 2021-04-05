# --------- import des librairies
import os
import sys
import sqlite3
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtCore, QtMultimedia
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDockWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap

import queue
import sounddevice as sd
from PyQt5.QtMultimedia import QAudioDeviceInfo, QAudio, QCameraInfo

input_audio_deviceInfos = QAudioDeviceInfo.availableDevices(QAudio.AudioInput)


baseDeDonnees = sqlite3.connect('labase.db')
curseur = baseDeDonnees.cursor()
curseur.execute("SELECT * FROM liste_1")

app = QApplication(sys.argv)
recorder = QtMultimedia.QAudioRecorder()
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(CURRENT_DIR, "test.mp3")
settings = QtMultimedia.QAudioEncoderSettings()
settings.setEncodingMode(QtMultimedia.QMultimedia.ConstantBitRateEncoding)
selected_codec = "audio/pcm"
settings.setCodec(selected_codec)
#bit_rate = 3200  # other values: 32000, 64000,96000, 128000
#settings.setBitRate(bit_rate)
settings.setQuality(QtMultimedia.QMultimedia.VeryHighQuality)
selected_container = "audio/x-wav"
recorder.setEncodingSettings(settings, QtMultimedia.QVideoEncoderSettings(), selected_container)
recorder.setOutputLocation(QtCore.QUrl.fromLocalFile(filename))

# open qss file
File = open("Photoxo.qss", 'r')


device = 0
downsample = 1


device_info = sd.query_devices(device, 'input')
samplerate = device_info['default_samplerate']
sd.default.samplerate = samplerate


with File:
    qss = File.read()
    app.setStyleSheet(qss)


def update_now(value):
    device = devices_list.index(value)
    print('Device:', devices_list.index(value))

def getAudio():
    try:
        def audio_callback(indata, frames, time, status):
            q.put(indata[::downsample, [0]])

        stream = sd.InputStream(device=device, channels=max(channels), samplerate=samplerate,callback=audio_callback)
        with stream:
            input()
    except Exception as e:
        print("ERROR: ", e)

def getFile(valeur):
    baseDeDonnees = sqlite3.connect('labase.db')
    curseur = baseDeDonnees.cursor()
    print("Connexion reussie a SQLite")
    print("select image from liste_1 where valeur_liste='{}'".format(valeur))
    photos = curseur.execute("select image from liste_1 where valeur_liste='{}'".format(valeur))

    for photo in photos:
        pm = QPixmap()
        pm.loadFromData(photo[0])
        ui.lbl_img.setPixmap(QPixmap(pm))

    baseDeDonnees.close()


def quitte():
    sys.exit(app.exec_())
    # app.quit()
    # sys.exit()


def widj():
    # ui.dockWidget.show()
    filePath, flag = QFileDialog.getOpenFileName(ui, 'Sélection de fichier''./', 'FLOWS(*.txt *.text *.flow)')
    print(filePath, flag)
    file = open(filePath, "r")
    ui.txt_zone_txt.setPlainText(file.read())
    # print(FilePath.read())
    file.close()


def ok():
    print(ui.lineEdit.text())


def apropos():
    dlg = QMessageBox(ui)

    dlg.setFixedSize(411, 247)
    dlg.setWindowIcon(QtGui.QIcon('phm.png'))
    dlg.setText("Copyright Phoebus du F.L.A.L.")
    dlg.setWindowTitle("A propos !")
    # dlg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
    dlg.exec_()

def showTime():
    timer.stop()
    ui_propos.close()
    ui.show()




def listview_clicked():
    item = ui.listWidget.currentItem()
    baseDeDonnees = sqlite3.connect('labase.db')
    curseur = baseDeDonnees.cursor()
    curseur.execute("select valeur_liste from liste_1 where nom_liste_1='{}'".format(item.text()))
    contact = curseur.fetchone()
    print(contact[0])
    getFile(contact[0])


def enregistre_sous():
    name, ext = QFileDialog.getSaveFileName(ui, 'Enregistrer sous', '', ' FLOWS(*.txt *.text *.flow)', )
    if name != "":
        file = open(str(name), 'w')
        text = "tata"
        file.write(text)
        file.close()


def stop():
    print("stop")
    recorder.stop()

def lire():
    print("record")
    recorder.record()

# ------- gestion de la fenetre a propos ------
timer = QTimer()
timer.timeout.connect(showTime)
timer.start(2000)

ui_propos  = uic.loadUi("apropos.ui")
ui_propos.show()

# --------- fin de  a propos -------

ui = uic.loadUi("menu_bar.ui")
ui.setWindowIcon(QtGui.QIcon('phm.png'))
ui.statusbar.showMessage("Copyright Phoebus du F.L.A.L.");
#ui.show()


ui.actionQuitter.triggered.connect(quitte)
ui.actionOuvrir.triggered.connect(widj)
ui.actionEnregistrer_sous.triggered.connect(enregistre_sous)
ui.btn_ok.clicked.connect(ok)
ui.actionA_propos.triggered.connect(apropos)
ui.btn_lire.clicked.connect(lire)
ui.btn_stop.clicked.connect(stop)

ui.listWidget.clicked.connect(listview_clicked)

# ------- nourrissage liste ------------
for liste in curseur.fetchall():
    ui.listWidget.addItem(str(liste[1]))
baseDeDonnees.close()

docker = QDockWidget(ui)
docker.setWindowTitle("un doc en plus")
docker.setAllowedAreas(Qt.RightDockWidgetArea)
docker.setGeometry(100, 26, 200, 30)
docker.resize(320, 240)
docker.setMinimumSize(320, 240)
docker.setFloating(False)
docker.setStyleSheet('background-color:gray')
docker.show()

for doc in ui.findChildren(QDockWidget):
    print(str(doc.windowTitle()))
    ui.menuAffichage.addAction(doc.toggleViewAction())

# ui.___.connect(traite)
# ui.___.clicked.connect(ajouter)
devices_list = []
for device in input_audio_deviceInfos:
    devices_list.append(device.deviceName())
ui.comboBox.addItems(devices_list)
ui.comboBox.currentIndexChanged['QString'].connect(update_now)
ui.comboBox.setCurrentIndex(0)


sys.exit(app.exec_())
