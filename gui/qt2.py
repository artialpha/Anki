# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from aqt import mw
from PyQt5.QtWidgets import QMessageBox

from .api_eng import create_cards as cr

api_file = "api_file.TXT"
api_path = os.path.dirname(os.path.realpath(__file__))
api_path = api_path + "\\" + api_file


class WorkerThreadGet(QThread):
    update_text = pyqtSignal(str)
    update_message = pyqtSignal(str)

    def __init__(self, typ, gui):
        super().__init__()
        self.typ = typ
        self.gui = gui

    def run(self):
        words = self.gui.text_def.toPlainText()
        words = words.splitlines()

        self.gui.label.setText("wait...")
        self.gui.button_meaning.setEnabled(False)
        self.gui.button_phrasals.setEnabled(False)
        self.gui.button_multiple.setEnabled(False)
        self.gui.button_definition.setEnabled(False)
        self.gui.button_phr_get.setEnabled(False)
        self.gui.button_phrases.setEnabled(False)

        endpoint = "entries"
        language_code = "en-us"

        if self.typ == 'def':
            create = cr.CreateCards(self.gui.app_id, self.gui.app_key, endpoint, language_code)
            content, message = create.get_definitions(words).values()


        elif self.typ == 'phr':
            create = cr.CreateCards(self.gui.app_id, self.gui.app_key, endpoint, language_code)
            content = create.get_phrases(words)

        self.update_text.emit(content)
        self.update_message.emit(message)
        self.gui.label.setText("done!")


class WorkerThreadCreate(QThread):
    def __init__(self, typ, gui):
        super().__init__()
        self.typ = typ
        self.gui = gui

    def run(self):
        self.gui.label.setText("wait, cards are being created")
        self.gui.button_meaning.setEnabled(False)
        self.gui.button_phrasals.setEnabled(False)
        self.gui.button_multiple.setEnabled(False)
        self.gui.button_definition.setEnabled(False)
        self.gui.button_phr_get.setEnabled(False)
        self.gui.button_phrases.setEnabled(False)
        file = "file.TXT"
        path = os.path.dirname(os.path.realpath(__file__))
        path = path + "\\" + file

        # here i should return the value of the word that has no results
        self.gui.create_cards(self.gui.text_create.toPlainText(), path, self.typ)

        # select deck
        did = mw.col.decks.id("test")
        mw.col.decks.select(did)

        # anki defaults to the last note type used in the selected deck
        m = mw.col.models.byName("word formation")
        deck = mw.col.decks.get(did)
        deck['mid'] = m['id']
        mw.col.decks.save(deck)

        # and puts cards in the last deck used by the note type
        m['did'] = did
        mw.col.models.save(m)
        self.gui.label.setText("done!")


class Ui_Form(QtWidgets.QWidget, object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 449)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 91, 31))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.box_language = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.box_language.setObjectName("box_language")
        self.box_language.addItem("")
        self.box_language.addItem("")
        self.verticalLayout.addWidget(self.box_language)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 210, 481, 131))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(30, 15, 30, 5)
        self.horizontalLayout.setSpacing(100)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.text_create = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.text_create.setObjectName("text_create")
        self.horizontalLayout.addWidget(self.text_create)
        self.text_def = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.text_def.setObjectName("text_def")
        self.horizontalLayout.addWidget(self.text_def)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(9, 360, 239, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_meaning = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.button_meaning.setObjectName("button_meaning")
        self.horizontalLayout_2.addWidget(self.button_meaning)
        self.button_phrasals = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.button_phrasals.setObjectName("button_phrasals")
        self.horizontalLayout_2.addWidget(self.button_phrasals)
        self.button_multiple = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.button_multiple.setObjectName("button_multiple")
        self.horizontalLayout_2.addWidget(self.button_multiple)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(269, 360, 226, 31))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(10, 0, 10, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.button_definition = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.button_definition.setObjectName("button_definition")
        self.horizontalLayout_3.addWidget(self.button_definition)
        self.button_phr_get = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.button_phr_get.setObjectName("button_phr_get")
        self.horizontalLayout_3.addWidget(self.button_phr_get)
        self.label_def = QtWidgets.QLabel(Form)
        self.label_def.setGeometry(QtCore.QRect(330, 190, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_def.setFont(font)
        self.label_def.setObjectName("label_def")
        self.label_create = QtWidgets.QLabel(Form)
        self.label_create.setGeometry(QtCore.QRect(70, 190, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_create.setFont(font)
        self.label_create.setObjectName("label_create")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(90, 340, 81, 16))
        self.label.setObjectName("label")
        self.text_app_id = QtWidgets.QPlainTextEdit(Form)
        self.text_app_id.setGeometry(QtCore.QRect(140, 50, 261, 31))
        self.text_app_id.setObjectName("text_app_id")
        self.text_app_key = QtWidgets.QPlainTextEdit(Form)
        self.text_app_key.setGeometry(QtCore.QRect(140, 90, 261, 31))
        self.text_app_key.setObjectName("text_app_key")
        self.label_app_id = QtWidgets.QLabel(Form)
        self.label_app_id.setGeometry(QtCore.QRect(90, 60, 47, 13))
        self.label_app_id.setObjectName("label_app_id")
        self.label_app_key = QtWidgets.QLabel(Form)
        self.label_app_key.setGeometry(QtCore.QRect(90, 100, 47, 13))
        self.label_app_key.setObjectName("label_app_key")
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(0, 30, 531, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setGeometry(QtCore.QRect(0, 160, 531, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.button_api = QtWidgets.QPushButton(Form)
        self.button_api.setGeometry(QtCore.QRect(220, 130, 75, 23))
        self.button_api.setObjectName("button_api")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 400, 77, 25))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.button_phrases = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.button_phrases.setObjectName("button_phrases")
        self.horizontalLayout_4.addWidget(self.button_phrases)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.button_meaning.clicked.connect(lambda: self.on_click('all'))
        self.button_phrasals.clicked.connect(lambda: self.on_click('phrasal'))
        self.button_multiple.clicked.connect(lambda: self.on_click('abcd'))
        self.button_phrases.clicked.connect(lambda: self.on_click('phrases'))

        self.button_definition.clicked.connect(lambda: self.get('def'))
        self.button_phr_get.clicked.connect(lambda: self.get('phr'))

        self.button_api.clicked.connect(lambda: self.add_data_api())

        if os.path.exists(api_path):
            with open(api_path) as f:
                content = f.readlines()
                if content:
                    self.app_id = content[0].strip('\n')
                    self.app_key = content [1]
                    self.text_app_id.insertPlainText(self.app_id)
                    self.text_app_key.insertPlainText(self.app_key)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.box_language.setItemText(0, _translate("Form", "english"))
        self.box_language.setItemText(1, _translate("Form", "german"))
        self.button_meaning.setText(_translate("Form", "all meanings"))
        self.button_phrasals.setText(_translate("Form", "phrasals"))
        self.button_multiple.setText(_translate("Form", "abcd"))
        self.button_definition.setText(_translate("Form", "get definition"))
        self.button_phr_get.setText(_translate("Form", "get phrases"))
        self.label_def.setText(_translate("Form", "word definition"))
        self.label_create.setText(_translate("Form", "create cards"))
        self.label.setText(_translate("Form", "you can add..."))
        self.label_app_id.setText(_translate("Form", "app id:"))
        self.label_app_key.setText(_translate("Form", "app key:"))
        self.button_api.setText(_translate("Form", "add data"))
        self.button_phrases.setText(_translate("Form", "phrases"))

    def add_data_api(self):
        with open(api_path, 'w+') as f:
            self.app_id = self.text_app_id.toPlainText()
            self.app_key = self.text_app_key.toPlainText()

            f.write(self.app_id + '\n')
            f.write(self.app_key)

    def on_click(self, typ):
        self.worker = WorkerThreadCreate(typ, self)
        self.worker.start()
        self.worker.finished.connect(self.create_cards_finished)

    def create_cards_finished(self):
        self.button_meaning.setEnabled(True)
        self.button_phrasals.setEnabled(True)
        self.button_multiple.setEnabled(True)
        self.button_definition.setEnabled(True)
        self.button_phr_get.setEnabled(True)
        self.button_phrases.setEnabled(True)

    def create_cards(self, list_words, path, type):
        endpoint = "entries"
        language_code = "en-us"

        create = cr.CreateCards(self.app_id, self.app_key, endpoint, language_code)
        if type == 'all':
            create.multiple_cards(self.list_of_words(list_words), path)
        elif type == 'phrasal':
            create.create_phrasals(self.list_of_words(list_words), path)
        elif type == 'abcd':
            lines = list_words.splitlines()
            for line in lines:
                create.create_abcd(line, path)
        elif type == 'phrases':
            create.create_phrases(self.list_of_words(list_words), path)

    def get(self, typ):
        self.worker = WorkerThreadGet(typ, self)
        self.worker.start()

        self.worker.finished.connect(self.create_cards_finished)
        self.worker.update_text.connect(self.update_area)
        self.worker.update_message.connect(self.update_message)

    def update_area(self, val):
        self.text_def.clear()
        self.text_def.insertHtml(val)

    def update_message(self, val):
        if val:
            QMessageBox.about(self, "Title", val)



    @staticmethod
    def list_of_words(text):
        list_words = text.splitlines()
        return [x.strip().split() for x in list_words]


