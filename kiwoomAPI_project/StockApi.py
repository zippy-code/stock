from PyQt5.QAxContainer import *

'''
ocx: OLE custom control - 하나의 객체 연결 및 포함 맞춤형 컨트롤, 윈도우에서 수행되는 응용프로그램에서 사용되기 위해 만들어질 수 있는
                          특수목적 프로그램
OLE: Object Linking and Embedding - 문서와 기타 객체의 연결과 삽입을 도와준다.
'''

class StockApi:
    def __init__(self):
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.handle_login)
        self.ocx.OnReceiveTrData.connect(self.receive_trdata)
        self.dic_callback_funcs = {
            "login" : None
            , "stock_code_data": None
        }

    # 키움 API 접속 CommConnect() 함수 호출
    def CommConnect(self, callback_func = None):
        self.ocx.dynamicCall("CommConnect()")
        if callable(callback_func):      # callback 함수가 있다면 등록
            self.dic_callback_funcs['login'] = callback_func 

    # 로그인 성공, 실패 여부 반환값 전달.
    def handle_login(self, err_code):
        callback_func = self.dic_callback_funcs['login']
        if callable(callback_func):      # callback 함수가 있다면 호출 
            callback_func(err_code=err_code)
    
    # 로그인 성공, 실패 여부 확인.
    def check_login_state(self, dic_check_login):
        if self.ocx.dynamicCall("GetConnectState()") != 0:
           dic_check_login["is_login"] = True

    # 종목 코드에 대한 데이터 확인을 위한 함수
    def get_trd_data(self, code, callback_func = None):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001", 0, "0101")

        if callable(callback_func):
            self.dic_callback_funcs['stock_code_data'] = callback_func

    # CommRqData() 함수 호출에 대한 응답.
    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2): 
        if rqname == "opt10001_req":
                name = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "종목명")
                volume = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "거래량")

        callback_func = self.dic_callback_funcs['stock_code_data']
        if callable(callback_func):      # callback 함수가 있다면 호출 
            callback_func(name=name, volume=volume)

    # 종목 코드 리스트 확인.
    def get_code_list(self, code_name_list):
        ret = self.ocx.dynamicCall("GetCodeListByMarket(QString)", ["0"])
        code_list = ret.split(';')
        
        for x in code_list:
            name = self.ocx.dynamicCall("GetMasterCodeName(QString)", [x])
            code_name_list.append(x + " : " + name)

    #내 계좌 정보 확인
    def get_my_account_info(self, dic_my_account):
        account_num = self.ocx.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
        dic_my_account["account"] = account_num

    #테마 그룹 얻기
    def get_theme_group_list(self):
        ret = self.ocx.dynamicCall("GetThemeGroupList(int)", 1)
        group_list = ret.split(';')
        
        return group_list