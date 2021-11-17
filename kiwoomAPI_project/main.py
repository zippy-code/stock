import sys
from PyQt5.QtWidgets import *
from PyQt5 import *
from StockApi import *

dic_check_login = {"is_login": False}

def global_object():
    global stockApi 
    stockApi = StockApi()

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global_object()
        self.setGeometry(300, 300, 300, 300)
        
        login_btn = QPushButton("Login", self)
        login_btn.move(20, 20)
        
        stockCodeBtn = QPushButton("Get Code", self)
        stockCodeBtn.move(20, 70)

        stockCodeLstBtn = QPushButton("Get Code List", self)
        stockCodeLstBtn.resize(140, 30)
        stockCodeLstBtn.move(20, 120)

        get_my_account_info = QPushButton("account info", self)
        get_my_account_info.resize(140, 30)
        get_my_account_info.move(20, 170)
        
        get_theme_group_list = QPushButton("theme group list", self)
        get_theme_group_list.resize(160, 30)
        get_theme_group_list.move(20, 220)

        login_btn.clicked.connect(self.click_loginBtn)
        stockCodeBtn.clicked.connect(self.click_stockCodeBtn)
        stockCodeLstBtn.clicked.connect(self.click_stockListBtn)
        get_my_account_info.clicked.connect(self.click_AccountInfoBtn)
        get_theme_group_list.clicked.connect(self.click_GroupListBtn)

    def click_loginBtn(self):
        stockApi.CommConnect(self.callback_login)

    def callback_login(self, *args, **kwargs):
        if kwargs['err_code'] == 0:
            self.statusBar().showMessage("Success Login")
    
    def click_stockCodeBtn(self):
        stockApi.check_login_state(dic_check_login)

        if dic_check_login["is_login"] == False:
            self.statusBar().showMessage("Login plz.")
        else:
            self.getCode = GetCode()
            self.getCode.show()
            #self.getCode.showModal()
    
    def click_stockListBtn(self):
        stockApi.check_login_state(dic_check_login)

        if dic_check_login["is_login"] == False:
            self.statusBar().showMessage("Login plz.")
        else:
            self.getCodeLst = GetCodeLst()
            self.getCodeLst.show()
    
    def click_AccountInfoBtn(self):
        stockApi.check_login_state(dic_check_login)

        if dic_check_login["is_login"] == False:
            self.statusBar().showMessage("Login plz.")
        else:
            self.getAccInfo = GetAccountInfo()
            self.getAccInfo.show()
    
    def click_GroupListBtn(self):
        stockApi.check_login_state(dic_check_login)

        if dic_check_login["is_login"] == False:
            self.statusBar().showMessage("Login plz.")
        else:
            self.geThemeGroupList = GetThemeGroupList()
            self.geThemeGroupList.show()


class GetCode(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sub Window')
        self.setGeometry(300, 300, 500, 200)

        label = QLabel('종목코드: ', self)
        label.move(20, 21)

        self.code_edit = QLineEdit(self)
        self.code_edit.move(100, 19)

        getCodeBtn = QPushButton("조회", self)
        getCodeBtn.move(310, 16)
        getCodeBtn.clicked.connect(self.btn_clicked)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 60, 410, 100)
        self.text_edit.setEnabled(False)

    def btn_clicked(self):
        self.text_edit.clear()
        code = self.code_edit.text()
        stockApi.get_trd_data(code, self.handle_stock_code_data)
        self.text_edit.append("종목코드: " + code)
            
    def handle_stock_code_data(self, **kwargs):
        self.text_edit.append("종목명: " + kwargs['name'].strip())
        self.text_edit.append("거래량: " + kwargs['volume'].strip())

    def showModal(self, *args, **kwargs):
        return super().exec_()


class GetCodeLst(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sub Window')
        self.setGeometry(300, 300, 650, 220)

        get_code_list_btn = QPushButton("Get Code List", self)
        get_code_list_btn.resize(140, 30)
        get_code_list_btn.move(490, 20)
        get_code_list_btn.clicked.connect(self.btn_clicked)

        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(10, 10, 450, 200)
    
    def btn_clicked(self):
        code_name_list = []
        stockApi.get_code_list(code_name_list)
        self.listWidget.addItems(code_name_list)

class GetAccountInfo(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sub Window')
        self.setGeometry(300, 300, 500, 300)

        getAccInfoBtn = QPushButton("Check info", self)
        getAccInfoBtn.move(310, 16)
        getAccInfoBtn.clicked.connect(self.btn_clicked)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 60, 410, 100)

    def btn_clicked(self):
        self.text_edit.clear()
        dic_my_account = {"account": ""}
        stockApi.get_my_account_info(dic_my_account)
        self.text_edit.append("계좌번호: " + dic_my_account["account"].rstrip(';'))
    
class GetThemeGroupList(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sub Window')
        self.setGeometry(300, 300, 650, 220)

        get_group_list = QPushButton("Get Code List", self)
        get_group_list.resize(140, 30)
        get_group_list.move(490, 20)
        get_group_list.clicked.connect(self.btn_clicked)

        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(10, 10, 450, 200)

    def btn_clicked(self):
        group_lsit = stockApi.get_theme_group_list()
        self.listWidget.addItems(group_lsit)
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()