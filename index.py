import sys, os
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QLabel,\
    QLineEdit)
from PyQt5.QtGui import QFont, QIcon
import sqlite3

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''Процедура генерации окна'''

        #задаем параметры главного окна
        self.setGeometry(700, 300, 500, 310)
        self.setWindowTitle('ЭРП')
        self.setWindowIcon(QIcon('icon.png'))

        #создаем кнопку 'Внести изменения'
        btn_make_changes = QPushButton('Внести изменения', self)
        btn_make_changes.setToolTip('Внести изменения')
        btn_make_changes.resize(btn_make_changes.sizeHint())
        btn_make_changes.move(370, 270)
        btn_make_changes.clicked.connect(self.btn_make_changes_action)

        #BEGIN /// создаем поля

        bts_parameters = QLabel(self)
        bts_parameters.setText('Параметры BTS')
        bts_parameters.move(10,10)
        bts_parameters.setFont(QFont('Arial', 10, weight=QFont.Bold))

        bts_number = QLabel(self)
        bts_number.setText('BTS_56_:')
        bts_number.move(10,40)
        bts_number.setFont(QFont('Arial', 10))
        self.bts_number_input = QLineEdit(self)
        self.bts_number_input.move(90, 40)

        port_number = QLabel(self)
        port_number.setText('Порт TN_:')
        port_number.move(10,70)
        port_number.setFont(QFont('Arial', 10))
        port_number_input = QLineEdit(self)
        port_number_input.move(90, 70)

        # параметры SFTP
        sftp_parameters = QLabel(self)
        sftp_parameters.setText('Параметры SFTP')
        sftp_parameters.move(10,110)
        sftp_parameters.setFont(QFont('Arial', 10, weight=QFont.Bold))

        sftp_user = QLabel(self)
        sftp_user.setText('Пользователь:')
        sftp_user.move(10,140)
        sftp_user.setFont(QFont('Arial', 10))
        sftp_user_input = QLineEdit(self)
        sftp_user_input.move(130, 140)

        sftp_password = QLabel(self)
        sftp_password.setText('Пароль:')
        sftp_password.move(10,170)
        sftp_password.setFont(QFont('Arial', 10))
        sftp_password_input = QLineEdit(self)
        sftp_password_input.move(75, 170)

        sftp_port = QLabel(self)
        sftp_port.setText('Порт:')
        sftp_port.move(10,200)
        sftp_port.setFont(QFont('Arial', 10))
        sftp_port_input = QLineEdit(self)
        sftp_port_input.move(55, 200)

        sftp_root_path = QLabel(self)
        sftp_root_path.setText('Корневой путь:')
        sftp_root_path.move(10,230)
        sftp_root_path.setFont(QFont('Arial', 10))
        sftp_root_path_input = QLineEdit(self)
        sftp_root_path_input.move(130, 230)
        sftp_root_path_input.setGeometry(130, 230, 250, 25)

        #END /// создаем поля
        
        self.check_db_exists()

        self.show()


    def show_messagebox(self, message):
        messageBox = QMessageBox(self)
        messageBox.setWindowIcon(QIcon('icon.png'))
        messageBox.setWindowTitle('Предупреждение')
        messageBox.setIcon(QMessageBox.Question)
        messageBox.setText(f'{message}')        
        btn_yes = messageBox.addButton('Понял', QMessageBox.YesRole)      
        messageBox.exec_()

    def check_db_exists(self):
        if os.path.isfile('bts.db') is False:
            print('База данных не найдена!')
            self.show_messagebox('Файл базы данных bts.db не найден!\nЗапустите файл convert_xls_to_db.exe')

    def btn_make_changes_action(self):
        '''Действие для кнопки "Внести изменения"'''
        bts_number = self.bts_number_input.text()
        if bts_number == '':
            print('Пустое значение поля Номер BTS')
            self.show_messagebox('Вы не ввели номер BTS!')
        else:
            print('BTS_NUMBER:', bts_number)
            
            conn = sqlite3.connect('bts.db')
            cur = conn.cursor()
            try:
                bts_attributes = cur.execute(f'SELECT * FROM BTS WHERE bts_name = "{bts_number}"').fetchone()
                bts_name = bts_attributes[0]
                bts_oam = bts_attributes[1]
                bts_ip_bts = bts_attributes[2]
                bts_ip_mbh = bts_attributes[3]
                print(bts_name, bts_oam, bts_ip_bts, bts_ip_mbh)
            except Exception:
                print('Такой BTS нет в базе данных!')
                self.show_messagebox('Такой BTS нет в базе данных!')

            
        

if __name__ == '__main__':
    '''Основная процедура'''

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())