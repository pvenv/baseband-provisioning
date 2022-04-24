import sys, os
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QLabel,\
    QLineEdit, QFileDialog)
from PyQt5.QtGui import QFont, QIcon
import sqlite3
from PyQt5 import uic

from lib.base import replace_atributes_in_files

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.window = Window()
        self.form = Form()
        self.form.setupUi(self.window)

        self.initUI()

    def initUI(self):
        '''Процедура генерации окна'''

        self.window.setWindowIcon(QIcon('icon.png'))
        self.window.show()

        self.form.btnLoad.clicked.connect(self.btn_load_action)
        self.form.btnSftpPath.clicked.connect(self.get_sftp_directory)
        self.check_db_exists()

    def show_messagebox(self, message):
        messageBox = QMessageBox(self)
        messageBox.setWindowIcon(QIcon('icon.png'))
        messageBox.setWindowTitle('Предупреждение')
        messageBox.setIcon(QMessageBox.Question)
        messageBox.setText(f'{message}')        
        btn_yes = messageBox.addButton('Понял', QMessageBox.YesRole)      
        messageBox.exec_()

    def get_sftp_directory(self):
        current_path = os.path.abspath(os.path.curdir)
        dirlist = QFileDialog.getExistingDirectory(self,"Выбрать папку корня SFTP",".")\
            .replace('/','\\')\
            .replace(f'{current_path}', '.')
        self.form.plainTextEdit.appendHtml("Выбран новый корень SFTP: <b>{}</b>".format(dirlist))

    def check_db_exists(self):
        if os.path.isfile('bts.db') is False:
            self.form.plainTextEdit.appendHtml('Файл базы данных bts.db не найден!\nЗапустите файл convert_xls_to_db.exe')

    def check_sftp_dir(self):
        if os.path.isdir(f'{self.form.sftp_path_input.text()}'.replace('\\.', '')) is False:
            self.form.plainTextEdit.appendHtml(f'Путь {self.form.sftp_path_input.text()} не найден, выберите новый путь!')
            return False

    def btn_load_action(self):
        '''Действие для кнопки "Внести изменения"'''
        bts_number = self.form.bts_number_input.text()
        if bts_number == '':
            self.form.plainTextEdit.appendHtml('Вы не ввели номер BTS!')
            return
            
        tn_port = self.form.tn_port_input.text()
        if tn_port == '':
            self.form.plainTextEdit.appendHtml('Вы не ввели порт TN!')
            return

        if self.check_sftp_dir() is False:
            return
        
        conn = sqlite3.connect('bts.db')
        cur = conn.cursor()
        try:
            bts_attributes = cur.execute(f'SELECT * FROM BTS WHERE bts_name = "{bts_number}"').fetchone()
            bts_name = bts_attributes[0]
            bts_oam = bts_attributes[1]
            bts_ip_bts = bts_attributes[2]
            bts_ip_mbh = bts_attributes[3]
            print(bts_name, bts_oam, bts_ip_bts, bts_ip_mbh)

            replace_atributes_in_files(self, bts_name, bts_oam, bts_ip_bts, bts_ip_mbh, tn_port)

        except Exception:
            self.form.plainTextEdit.appendHtml('Такой BTS нет в базе данных!')

            
        

if __name__ == '__main__':
    '''Основная процедура'''

    Form, Window = uic.loadUiType("index.ui")
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())