import random, sys
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from  os import path
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from SplashScreen import Ui_splashscreen
from PyQt5 import QtCore,QtGui
import MySQLdb
from PyQt5.QtGui import QCursor, QWindow
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
from PyQt5.QtCore import *

###### Globla var######
counter = 0
GLOBAL_STATE = 0
kero=1
###################

##call ui screens##
FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),'New folder\/banking system2.ui'))
login,_=loadUiType(path.join(path.dirname(__file__),'New folder\login.ui'))
###################

#########log_in handle##########
class Login(QWidget , login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(self.shadow)

        self.pushButton.clicked.connect(self.Handel_Login)
        self.Close.clicked.connect(QApplication.instance().quit)
        self.Minimize.clicked.connect(self.min)
        self.Restrore_down.clicked.connect(self.max)

        style = open('themes/darkorange.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)
    def min(self):
        self.showMinimized()
    def max(self):
        global kero
        if kero%2!=0:
            self.setGeometry(-10,-10,1920,1030)  
            self.dropShadowFrame.resize(1920,1030)
            self.lineEdit.setGeometry(730,400,301,41)
            self.lineEdit_2.setGeometry(730,450,301,41)
            self.label.setGeometry(700,500,401,31)
            self.pushButton.setGeometry(800,540,161,51)
            self.label_credits.setGeometry(350,630,621,51)

            kero+=1
        else:
            self.setGeometry(615,312,690,405)
            self.lineEdit.setGeometry(180,100,301,41)
            self.lineEdit_2.setGeometry(180,150,301,41)
            self.label.setGeometry(140,200,401,31)
            self.pushButton.setGeometry(240,240,161,51)
            self.label_credits.setGeometry(-210,350,621,21)
            kero+=1


    def Handel_Login(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='123456' , db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        sql = ''' SELECT * FROM users'''

        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data  :
            if username == row[1] and password == row[3]:
                print('user match')
                self.window2 = MainApp()
                self.close()
                self.window2.show()

            else:
                self.label.setText('Make Sure You Enterd Your Username And Password Correctly')
###############################

#############Banking class##################
class banking:

    _accounts = {}
    _name = "PyBank Inc"
    def Name(self):
        return self._name
    def GenerateAccountNumber(self):
        return random.randint(10000, 99999)
                
    def CreateAccount(self):
        acct_num = self.GenerateAccountNumber()
        user_name = self.GetUserName(self.username.text())
        if not user_name:
            return None
        
        deposit_amt = self.GetAmount("DEPOSIT",self.deposit.text())
        if not deposit_amt:
            return
        
        account = Account(user_name, acct_num, deposit_amt)
        self._accounts[acct_num] = account
        x=f"Savings account<strong style='color:#F5D244;'>#{account.AccountNumber}</strong> <br>has been created for customer <strong style='color:#F5D244;'>{account.Name}</strong><br> with opening balance of <strong style='color:#F5D244;'>${account.Balance:,.2f}</strong>."
        QMessageBox.about(self,"Done",x)
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.textBrowser_3.clear()
    def GetUserName(self,x):
        user_name = x.strip()
        if not user_name:
            QMessageBox.about(self,"Alert","Invalid user name")
            return None
        else:
            return user_name    
    
    def GetAmount(self, amount_type,x):
        amount = x
        try:
            amount = float(amount)
        except Exception:
            QMessageBox.about(self,"Alert","Invalid input")
            return None
        
        if amount <= 0:
            QMessageBox.about(self,"Alert","Invalid amount")
            return None
        
        return amount
    
    def Deposit(self):
        account = self.ValidateUser(self.le_tips_3.text(),self.le_tips_5.text())
        if not account:
            return
        
        deposit_amt = self.GetAmount("DEPOSIT",self.le_tips_4.text())
        if not deposit_amt:
            return
        
        account.Deposit(deposit_amt)
        self._accounts[account.AccountNumber] = account
        x=f"An deposit of <strong style='color:#F5D244;'>${deposit_amt:,.2f}</strong> <br>has been made to account <strong style='color:#F5D244;'>{account.AccountNumber} </strong><br>for a current balance of <strong style='color:#F5D244;'>${account.Balance:,.2f}</strong>." 
        QMessageBox.about(self,"Done",x)
    def ValidateUser(self,x,y):
        user_name = self.GetUserName(x)
        if not user_name:
            return None
        
        acct_num = self.GetAccountNumber(y)
        if not acct_num:
            return None
        
        account = self._accounts.get(acct_num, None)
        
        if not account:
            QMessageBox.about(self,"Alert","Invalid account number.")
            return None
        elif account.Name != user_name:
            QMessageBox.about(self,"Alert","Invalid user name")
            return None
        else:
            return account
    def GetAccountNumber(self,x):
        acct_num = x
        if not acct_num.isnumeric():            
            QMessageBox.about(self,"Alert","Invalid account number.")
            return None
        elif len(acct_num) != 5:
            QMessageBox.about(self,"Alert","Account number must be 5 digits")
            return None
        else:
            return int(acct_num)  
    def DisplayBalance(self):
        account = self.ValidateUser(self.le_tips_12.text(),self.le_tips_13.text())
        if account:
            x=f"Current balance  on account <strong style='color:#F5D244;'>{account.AccountNumber}</strong><br>is <strong style='color:#F5D244;'>{account.Balance:,.2f}</strong>"
            QMessageBox.about(self,"Done",x) 
    def Withdraw(self):
        account = self.ValidateUser(self.le_tips_7.text(),self.le_tips_8.text())
        if not account:
            return
        
        withdraw_amt = self.GetAmount("WITHDRAWAL",self.le_tips_6.text())
        if not withdraw_amt:
            return
        if int(self.le_tips_6.text())<= account._balance:
            account.Withdraw(withdraw_amt)
            self._accounts[account.AccountNumber] = account
            x=f"An withdrawal of <strong style='color:#F5D244;'>${withdraw_amt:,.2f}</strong><br>has been made to account <strong style='color:#F5D244;'>{account.AccountNumber}</strong><br>for a current balance of <strong style='color:#F5D244;'>${account.Balance:,.2f}</strong>."
            QMessageBox.about(self,"Done",x)
        else:
            QMessageBox.about(self,"Alert","Invalid withdrawal amount")

    def PrintAllAccounts(self):
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.textBrowser_3.clear()        
        for account in self._accounts.values():
            self.textBrowser_3.setPlainText(self.textBrowser_3.toPlainText()+"\n"+str(account.AccountNumber))
            self.textBrowser_2.setPlainText(self.textBrowser_2.toPlainText()+"\n"+str(account.Name))
            self.textBrowser.setPlainText(self.textBrowser.toPlainText()+"\n"+"$ "+str(account.Balance))

############ Accounts handle ############
class Account(banking):
    def __init__(self, name, acct_num, deposit):
        self._name = name
        self._account_number = acct_num
        self._balance = deposit
                                                                             

    @property
    def Balance(self):
        #balance is read only
        return self._balance

    @property
    def AccountNumber(self):
        #Account Number is read only
        return self._account_number
                                                                             
 
    @property
    def Name(self):
        return self._name

    @Name.setter
    def Name(self, value):
        self._name = value

    def Deposit(self, value):
        if value > 0:
            self._balance += value
        else:
            QMessageBox.about(self,"Alert","Invalid deposit amount")
    def Withdraw(self, value):
        if value <= self._balance:
            self._balance -= value

############ main App ############
class MainApp(QMainWindow ,FORM_CLASS,banking):
    def __init__(self,parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self) 
        
        QtCore.QTimer.singleShot(2000, lambda: self.equale.setText("❤😊 Welcome to KO BANK! 😊❤"))
        
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        #########
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(self.shadow)
        self.handle_ui()
        self.animationitems()
        self.click()
        self.move_window=False
  
    def handle_ui (self):
        self.setWindowTitle("keroo banking system")
        self.setWindowIcon(QIcon("i.png"))
        self.setFixedSize(1274,716)
        self.Move_Box_1()

##########Animations handle#########
###################################
    def animationitems(self):
        self.Move_Box_2()
        self.Move_Box_3()
        self.Move_Box_4()
        self.Move_Box_5()
        self.Move_Box_6()
        self.Move_Box_7()
    def Move_Box_1(self):
        box_animation1 = QPropertyAnimation(self.equale , b"geometry")
        box_animation1.setDuration(1000)
        box_animation1.setStartValue(QRect(100,160,561,0))
        box_animation1.setEndValue(QRect(100,160,561,161))
        box_animation1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation1.start()
        self.box_animation1 = box_animation1
        box_animation1_1 = QPropertyAnimation(self.start_btn , b"geometry")
        box_animation1_1.setDuration(1000)
        box_animation1_1.setStartValue(QRect(330,360,0,0))
        box_animation1_1.setEndValue(QRect(330,360,131,51))
        box_animation1_1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation1_1.start()
        self.box_animation1_1 = box_animation1_1
    def Move_Box_2(self):
        box_animation2 = QPropertyAnimation(self.pushButton_3 , b"geometry")
        box_animation2.setDuration(2000)
        box_animation2.setStartValue(QRect(900,160,88,61))
        box_animation2.setEndValue(QRect(980,160,88,61))
        box_animation2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation2.start()
        self.box_animation2 = box_animation2
    def Move_Box_3(self):
        box_animation3 = QPropertyAnimation(self.pushButton_9 , b"geometry")
        box_animation3.setDuration(2100)
        box_animation3.setStartValue(QRect(900,220,88,61))
        box_animation3.setEndValue(QRect(980,220,88,61))
        box_animation3.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation3.start()
        self.box_animation3 = box_animation3
    def Move_Box_4(self):
        box_animation4 = QPropertyAnimation(self.pushButton_7 , b"geometry")
        box_animation4.setDuration(2200)
        box_animation4.setStartValue(QRect(900,280,88,71))
        box_animation4.setEndValue(QRect(980,280,88,71))
        box_animation4.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation4.start()
        self.box_animation4 = box_animation4
    def Move_Box_5(self):
        box_animation5 = QPropertyAnimation(self.pushButton_6 , b"geometry")
        box_animation5.setDuration(2300)
        box_animation5.setStartValue(QRect(900,350,88,71))
        box_animation5.setEndValue(QRect(980,350,88,71))
        box_animation5.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation5.start()
        self.box_animation5 = box_animation5
    def Move_Box_6(self):
        box_animation6 = QPropertyAnimation(self.pushButton_8 , b"geometry")
        box_animation6.setDuration(2400)
        box_animation6.setStartValue(QRect(900,420,88,71))
        box_animation6.setEndValue(QRect(980,420,88,71))
        box_animation6.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation6.start()
        self.box_animation6 = box_animation6
    def Move_Box_7(self):
        box_animation7 = QPropertyAnimation(self.pushButton_13 , b"geometry")
        box_animation7.setDuration(2500)
        box_animation7.setStartValue(QRect(900,490,88,71))
        box_animation7.setEndValue(QRect(980,490,88,71))
        box_animation7.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation7.start()
        self.box_animation7 = box_animation7
    def Move_deposit(self):
        box_animation8 = QPropertyAnimation(self.label_8 , b"geometry")
        box_animation8.setDuration(2000)
        box_animation8.setStartValue(QRect(450,0,1221,661))
        box_animation8.setEndValue(QRect(40,0,1221,661))
        box_animation8.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation8.start()
        self.box_animation8 = box_animation8
        box_animation9 = QPropertyAnimation(self.label , b"geometry")
        box_animation9.setDuration(2500)
        box_animation9.setStartValue(QRect(130,420,641,501))
        box_animation9.setEndValue(QRect(130,190,641,501))
        box_animation9.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation9.start()
        self.box_animation9 = box_animation9
        box_animation10 = QPropertyAnimation(self.frame_5 , b"geometry")
        box_animation10.setDuration(2500)
        box_animation10.setStartValue(QRect(-400,120,401,80))
        box_animation10.setEndValue(QRect(20,120,401,80))
        box_animation10.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation10.start()
        self.box_animation10 = box_animation10
        box_animation11 = QPropertyAnimation(self.frame_6 , b"geometry")
        box_animation11.setDuration(2500)
        box_animation11.setStartValue(QRect(-400,220,401,80))
        box_animation11.setEndValue(QRect(30,220,401,80))
        box_animation11.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation11.start()
        self.box_animation11 = box_animation11
        box_animation12 = QPropertyAnimation(self.frame_7 , b"geometry")
        box_animation12.setDuration(2500)
        box_animation12.setStartValue(QRect(-400,320,401,80))
        box_animation12.setEndValue(QRect(10,320,401,80))
        box_animation12.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation12.start()
        self.box_animation12 = box_animation12
        box_animation13 = QPropertyAnimation(self.pushButton , b"geometry")
        box_animation13.setDuration(2500)
        box_animation13.setStartValue(QRect(110,440,0,0))
        box_animation13.setEndValue(QRect(110,440,181,41))
        box_animation13.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation13.start()
        self.box_animation13 = box_animation13
    def Move_createaccount(self):
        box_animation13 = QPropertyAnimation(self.frame_9 , b"geometry")
        box_animation13.setDuration(2000)
        box_animation13.setStartValue(QRect(240,-140,431,151))
        box_animation13.setEndValue(QRect(240,40,431,151))
        box_animation13.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation13.start()
        self.box_animation13 = box_animation13
        box_animation13_1 = QPropertyAnimation(self.frame_12 , b"geometry")
        box_animation13_1.setDuration(2100)
        box_animation13_1.setStartValue(QRect(280,230,341,0))
        box_animation13_1.setEndValue(QRect(280,230,341,61))
        box_animation13_1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation13_1.start()
        self.box_animation13_1 = box_animation13_1
        box_animation13_2 = QPropertyAnimation(self.frame_13 , b"geometry")
        box_animation13_2.setDuration(2200)
        box_animation13_2.setStartValue(QRect(290,300,331,0))
        box_animation13_2.setEndValue(QRect(290,300,331,71))
        box_animation13_2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation13_2.start()
        self.box_animation13_2 = box_animation13_2

        box_animation13_3 = QPropertyAnimation(self.btn_save , b"geometry")
        box_animation13_3.setDuration(2300)
        box_animation13_3.setStartValue(QRect(600,800,0,0))
        box_animation13_3.setEndValue(QRect(270,350,311,51))
        box_animation13_3.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation13_3.start()
        self.box_animation13_3 = box_animation13_3
        box_animation13_4 = QPropertyAnimation(self.btn_delete , b"geometry")
        box_animation13_4.setDuration(2400)
        box_animation13_4.setStartValue(QRect(600,800,0,0))
        box_animation13_4.setEndValue(QRect(270,420,311,51))
        box_animation13_4.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation13_4.start()
        self.box_animation13_4 = box_animation13_4  
    def Move_withdrawal(self):
        box_animation14 = QPropertyAnimation(self.label_2 , b"geometry")
        box_animation14.setDuration(1000)
        box_animation14.setStartValue(QRect(-310,560,531,371))
        box_animation14.setEndValue(QRect(0,260,531,371))
        box_animation14.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation14.start()
        self.box_animation14 = box_animation14
        box_animation14_1 = QPropertyAnimation(self.frame_15 , b"geometry")
        box_animation14_1.setDuration(2000)
        box_animation14_1.setStartValue(QRect(0,0,0,0))
        box_animation14_1.setEndValue(QRect(20,40,441,80))
        box_animation14_1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation14_1.start()
        self.box_animation14_1 = box_animation14_1
        box_animation14_2 = QPropertyAnimation(self.frame_16 , b"geometry")
        box_animation14_2.setDuration(2000)
        box_animation14_2.setStartValue(QRect(0,0,0,0))
        box_animation14_2.setEndValue(QRect(40,110,441,80))
        box_animation14_2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation14_2.start()
        self.box_animation14_2 = box_animation14_2
        box_animation14_3 = QPropertyAnimation(self.frame , b"geometry")
        box_animation14_3.setDuration(2000)
        box_animation14_3.setStartValue(QRect(0,0,0,0))
        box_animation14_3.setEndValue(QRect(20,190,441,80))
        box_animation14_3.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation14_3.start()
        self.box_animation14_3 = box_animation14_3
        box_animation14_4 = QPropertyAnimation(self.pushButton_2 , b"geometry")
        box_animation14_4.setDuration(2000)
        box_animation14_4.setStartValue(QRect(-310,560,531,371))
        box_animation14_4.setEndValue(QRect(150,300,181,41))
        box_animation14_4.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation14_4.start()
        self.box_animation14_4 = box_animation14_4
    def Move_balance(self):
        box_animation15 = QPropertyAnimation(self.label_3 , b"geometry")
        box_animation15.setDuration(2000)
        box_animation15.setStartValue(QRect(780,480,461,561))
        box_animation15.setEndValue(QRect(360,150,461,561))
        box_animation15.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation15.start()
        self.box_animation15 = box_animation15

        box_animation15_1 = QPropertyAnimation(self.label_4 , b"geometry")
        box_animation15_1.setDuration(1000)
        box_animation15_1.setStartValue(QRect(150,-200,1361,1011))
        box_animation15_1.setEndValue(QRect(-310,-200,1361,1011))
        box_animation15_1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation15_1.start()
        self.box_animation15_1 = box_animation15_1

        box_animation15_2 = QPropertyAnimation(self.frame_17 , b"geometry")
        box_animation15_2.setDuration(2100)
        box_animation15_2.setStartValue(QRect(0,0,0,0))
        box_animation15_2.setEndValue(QRect(30,120,451,80))
        box_animation15_2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation15_2.start()
        self.box_animation15_2 = box_animation15_2

        box_animation15_3 = QPropertyAnimation(self.frame_18 , b"geometry")
        box_animation15_3.setDuration(2200)
        box_animation15_3.setStartValue(QRect(0,0,0,0))
        box_animation15_3.setEndValue(QRect(20,220,411,80))
        box_animation15_3.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation15_3.start()
        self.box_animation15_3 = box_animation15_3

        box_animation15_4 = QPropertyAnimation(self.pushButton_5 , b"geometry")
        box_animation15_4.setDuration(2300)
        box_animation15_4.setStartValue(QRect(780,480,461,561))
        box_animation15_4.setEndValue(QRect(150,350,181,41))
        box_animation15_4.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation15_4.start()
        self.box_animation15_4 = box_animation15_4

        box_animation15_5 = QPropertyAnimation(self.power_27 , b"geometry")
        box_animation15_5.setDuration(2400)
        box_animation15_5.setStartValue(QRect(-190,550,201,211))
        box_animation15_5.setEndValue(QRect(-130,490,201,211))
        box_animation15_5.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        box_animation15_5.start()
        self.box_animation15_5 = box_animation15_5
    def Move_alluser(self):
            box_animation16 = QPropertyAnimation(self.textBrowser , b"geometry")
            box_animation16.setDuration(2000)
            box_animation16.setStartValue(QRect(320,100,291,26))
            box_animation16.setEndValue(QRect(320,100,291,331))
            box_animation16.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            box_animation16.start()
            self.box_animation16 = box_animation16

            box_animation16_1 = QPropertyAnimation(self.textBrowser_2 , b"geometry")
            box_animation16_1.setDuration(2200)
            box_animation16_1.setStartValue(QRect(160,100,161,26))
            box_animation16_1.setEndValue(QRect(160,100,161,331))
            box_animation16_1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            box_animation16_1.start()
            self.box_animation16_1 = box_animation16_1

            box_animation16_2 = QPropertyAnimation(self.textBrowser_3 , b"geometry")
            box_animation16_2.setDuration(2400)
            box_animation16_2.setStartValue(QRect(70,100,91,26))
            box_animation16_2.setEndValue(QRect(70,100,91,331))
            box_animation16_2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            box_animation16_2.start()
            self.box_animation16_2 = box_animation16_2

            box_animation16_3 = QPropertyAnimation(self.pushButton_4 , b"geometry")
            box_animation16_3.setDuration(2600)
            box_animation16_3.setStartValue(QRect(0,40,181,0))
            box_animation16_3.setEndValue(QRect(330,40,181,41))
            box_animation16_3.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            box_animation16_3.start()
            self.box_animation16_3 = box_animation16_3

#############################
    def click(self):
        self.quit_3.clicked.connect(self.close)
        self.btn_save.clicked.connect(self.CreateAccount)
        self.btn_delete.clicked.connect(self.deletedata)
        self.pushButton.clicked.connect(self.Deposit)
        self.pushButton_2.clicked.connect(self.Withdraw)
        self.pushButton_5.clicked.connect(self.DisplayBalance)
        self.pushButton_4.clicked.connect(self.PrintAllAccounts)
        self.pushButton_3.clicked.connect(self.create_account)
        self.pushButton_9.clicked.connect(self.deposit_)
        self.pushButton_7.clicked.connect(self.withdrawal)
        self.pushButton_6.clicked.connect(self.balance)
        self.pushButton_8.clicked.connect(self.alluser)
        self.pushButton_13.clicked.connect(self.close)
        self.start_btn.clicked.connect(self.startbtn)
        self.Close.clicked.connect(self.close)
        self.Minimize.clicked.connect(self.showMinimized)
    def startbtn(self):
        self.tabWidget.setCurrentIndex(1)
        self.Move_createaccount()
        self.animationitems
    def deletedata(self):
        self.username.setText("")
        self.deposit.setText("")
    def create_account(self):
        self.tabWidget.setCurrentIndex(1)
        self.label_39.setText("create an account")
        self.animationitems()
        self.Move_createaccount()
    def deposit_(self):
        self.tabWidget.setCurrentIndex(2)
        self.label_39.setText("make a deposit")
        self.animationitems()
        self.Move_deposit()
    def withdrawal(self):
        self.tabWidget.setCurrentIndex(3)
        self.label_39.setText("make a withdrawal")
        self.animationitems()
        self.Move_withdrawal()
    def balance(self):
        self.tabWidget.setCurrentIndex(4)
        self.label_39.setText("display balance")
        self.animationitems()
        self.Move_balance()

    def alluser(self):
        self.tabWidget.setCurrentIndex(5)
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.textBrowser_3.clear()        
        for account in self._accounts.values():
            self.textBrowser_3.setPlainText(self.textBrowser_3.toPlainText()+"\n"+str(account.AccountNumber))
            self.textBrowser_2.setPlainText(self.textBrowser_2.toPlainText()+"\n"+str(account.Name))
            self.textBrowser.setPlainText(self.textBrowser.toPlainText()+"\n"+"$ "+str(account.Balance))
        self.label_39.setText("display all accounts")
        self.animationitems()
        self.Move_alluser()
    def closeEvent(self,event):
    
        reply = QMessageBox.question(self, 'Message',"Are you sure to quit?", QMessageBox.Yes |QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class splashscreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui=Ui_splashscreen()
        self.ui.setupUi(self)
        #########
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        #########
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(self.shadow)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(35)

        self.ui.label_2.setText("<strong>WELCOME</strong> TO MY APPLICATION")
        # Change Texts
        QtCore.QTimer.singleShot(2000, lambda: self.ui.label_2.setText("<strong>LOADING</strong> DATABASE..."))
        QtCore.QTimer.singleShot(3100, lambda: self.ui.label_2.setText("<strong>LOADING</strong> USER INTERFACE..."))

        self.show()

    def progress(self):

        global counter
        # SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(counter)

        # CLOSE SPLASH SCREE AND OPEN APP
        if counter > 100:
            # STOP TIMER
            self.timer.stop()

            # SHOW MAIN WINDOW
            self.main = Login()
            self.main.show()

            # CLOSE SPLASH SCREEN
            self.close()

        # INCREASE COUNTER
        counter += 1

# def main():
#     app = QApplication(sys.argv)
#     window = MainApp()
#     window.show()
#     app.exec_()
def main():
    app2 = QApplication(sys.argv)
    window=splashscreen()
    sys.exit(app2.exec_())
if __name__ == '__main__':
    main()

